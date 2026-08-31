#!/usr/bin/env python3


import csv
import io
import json
import os
import queue
import re
import tempfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException


TOKEN_PATH = '/geri_connect/auth/v1/token'
PUBLIC_API_PREFIX = '/geri_connect/public/api/v1'
VIDEO_PATH = '/files/video.json/{session_uuid}/well{well_no}_zid{zid}.mp4'
VIDEO_ZIDS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '99']
DEFAULT_REQUEST_TIMEOUT = 30
DEFAULT_DOWNLOAD_TIMEOUT = 300
INPUT_COLUMN_ALIASES = {
    'patient_given_names': ['女方姓名'],
    'patient_name': ['男方姓名'],
    'no': ['no'],
}
OPTIONAL_INPUT_COLUMN_ALIASES = {
    'session_uuid': ['session_uuid'],
}


class CandlePublicClient:

    def __init__(self, base_url, username, password,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT,
                 download_timeout=DEFAULT_DOWNLOAD_TIMEOUT):
        self.base_url = base_url.rstrip('/')
        self.request_timeout = request_timeout
        self.download_timeout = download_timeout
        self.s = requests.Session()
        self.s.headers.update(self._get_auth_header(username, password))

    def _get_auth_header(self, username, password):
        url = urljoin(self.base_url, TOKEN_PATH)
        try:
            response = requests.get(url,
                                    auth=(username, password),
                                    verify=False,
                                    timeout=self.request_timeout)
            response.raise_for_status()
            token = response.json().get('token')
        except RequestException as ex:
            raise RuntimeError('IP 不通或用户名密码无法获取 auth: {}'.format(ex))
        except ValueError:
            raise RuntimeError('auth 接口返回内容不是 JSON。')

        if not token:
            raise RuntimeError('auth 接口没有返回 token，请检查用户名和密码。')
        return {'Authorization': 'Bearer {}'.format(token)}

    def get_dishrecords(self):
        return self._get_public_json('dishrecords')

    def get_sessionrecords(self, dish_uuid):
        return self._get_public_json('sessionrecords', {'dish_uuid': dish_uuid})

    def _get_public_json(self, endpoint, params=None):
        url = urljoin(self.base_url, PUBLIC_API_PREFIX + '/' + endpoint)
        try:
            response = self.s.get(url, params=params, verify=False, timeout=self.request_timeout)
            response.raise_for_status()
            body = response.json()
        except RequestException as ex:
            raise RuntimeError('接口请求失败 {}: {}'.format(endpoint, ex))
        except ValueError:
            raise RuntimeError('接口返回内容不是 JSON: {}'.format(endpoint))

        if body.get('error'):
            raise RuntimeError(body['error'])
        return body.get('content') or []

    def download_video(self, session_uuid, well_no, zid, output_path, overwrite=False):
        if os.path.exists(output_path) and not overwrite:
            return 'skipped'

        url = urljoin(self.base_url, VIDEO_PATH.format(session_uuid=session_uuid, well_no=well_no, zid=zid))
        try:
            response = self.s.get(url, stream=True, verify=False, timeout=self.download_timeout)
            response.raise_for_status()
            with open(output_path, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        video_file.write(chunk)
        except RequestException as ex:
            raise RuntimeError(ex)
        return 'downloaded'


def normalize(value):
    return (value or '').strip().lower()


def make_patient_key(patient_given_names, patient_name):
    return normalize(patient_given_names), normalize(patient_name)


def safe_filename(value):
    value = (value or '').strip()
    value = re.sub(r'[<>:"/\\|?*\r\n\t]+', '_', value)
    return value.strip(' ._') or 'unknown'


def resolve_input_columns(fieldnames):
    fieldnames = [str(name).strip() if name is not None else '' for name in (fieldnames or [])]
    resolved = {}

    for canonical, aliases in INPUT_COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in fieldnames:
                resolved[canonical] = alias
                break

    missing = [INPUT_COLUMN_ALIASES[key][0] for key in INPUT_COLUMN_ALIASES if key not in resolved]
    if missing:
        raise RuntimeError('Excel 缺少必需表头: {}'.format(', '.join(missing)))

    for canonical, aliases in OPTIONAL_INPUT_COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in fieldnames:
                resolved[canonical] = alias
                break
    return resolved


def canonicalize_target(row, columns):
    return {
        'patient_given_names': row.get(columns['patient_given_names'], ''),
        'patient_name': row.get(columns['patient_name'], ''),
        'no': row.get(columns['no'], ''),
        'session_uuid': row.get(columns['session_uuid'], '') if 'session_uuid' in columns else '',
    }


def read_csv_targets(csv_path):
    encodings = ['utf-8-sig', 'gb18030']
    last_error = None

    for encoding in encodings:
        try:
            with io.open(csv_path, 'r', encoding=encoding, newline='') as csv_file:
                sample = csv_file.read(4096)
                csv_file.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample) if sample else csv.excel
                except csv.Error:
                    dialect = csv.excel

                reader = csv.DictReader(csv_file, dialect=dialect)
                columns = resolve_input_columns(reader.fieldnames)
                return [canonicalize_target(row, columns) for row in reader]
        except UnicodeDecodeError as ex:
            last_error = ex

    if last_error:
        raise RuntimeError('CSV 编码无法识别，请保存为 UTF-8 或 GBK/GB18030 编码。')
    return []


def read_excel_targets(excel_path):
    try:
        from openpyxl import load_workbook
    except ImportError:
        raise RuntimeError('读取 Excel 需要 openpyxl，请在打包机器安装 openpyxl 后重新打包 exe。')

    workbook = load_workbook(excel_path, read_only=True, data_only=True)
    try:
        sheet = workbook.active
        rows = sheet.iter_rows(values_only=True)
        try:
            headers = next(rows)
        except StopIteration:
            return []

        fieldnames = [str(value).strip() if value is not None else '' for value in headers]
        columns = resolve_input_columns(fieldnames)
        column_indexes = {canonical: fieldnames.index(source) for canonical, source in columns.items()}

        targets = []
        for row in rows:
            row = row or []
            target = {}
            for canonical, index in column_indexes.items():
                value = row[index] if index < len(row) else ''
                target[canonical] = '' if value is None else str(value).strip()
            if any(target.values()):
                targets.append(target)
        return targets
    finally:
        workbook.close()


def display_value(value):
    value = (value or '').strip()
    return value or '<empty>'


def parse_well_no(value):
    value = (value or '').strip()
    if value.endswith('.0'):
        value = value[:-2]
    return value


def validate_targets(targets):
    if not targets:
        raise RuntimeError('Excel 没有可处理的数据行。')

    errors = []
    for index, target in enumerate(targets, start=2):
        patient_given_names = (target.get('patient_given_names') or '').strip()
        patient_name = (target.get('patient_name') or '').strip()
        well_no = parse_well_no(target.get('no'))
        if not patient_given_names:
            errors.append('第 {} 行缺少 女方姓名'.format(index))
        if not patient_name:
            errors.append('第 {} 行缺少 男方姓名'.format(index))
        if not well_no:
            errors.append('第 {} 行缺少 no'.format(index))
        elif not well_no.isdigit():
            errors.append('第 {} 行 no 不合法: {}'.format(index, display_value(well_no)))

    if errors:
        shown = errors[:20]
        if len(errors) > 20:
            shown.append('还有 {} 个错误未显示。'.format(len(errors) - 20))
        raise RuntimeError('Excel 数据预检失败:\n{}'.format('\n'.join(shown)))


def read_targets(input_path):
    extension = os.path.splitext(input_path)[1].lower()
    if extension in ['.xlsx', '.xlsm']:
        targets = read_excel_targets(input_path)
    elif extension == '.xls':
        raise RuntimeError('请先把 .xls 文件另存为 .xlsx 或 .csv 后再导入。')
    else:
        targets = read_csv_targets(input_path)
    validate_targets(targets)
    return targets


def check_output_dir_writable(output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    fd, test_path = tempfile.mkstemp(prefix='write_test_', suffix='.tmp', dir=output_dir)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as test_file:
            test_file.write('test')
    finally:
        if os.path.exists(test_path):
            os.remove(test_path)


def index_dishrecords(dishrecords):
    by_name = {}
    for dish in dishrecords:
        key = make_patient_key(dish.get('patient_given_names'), dish.get('patient_name'))
        by_name.setdefault(key, []).append(dish)
    return by_name


def make_video_filename(patient_given_names, patient_name, session_uuid, well_no, zid):
    return '{}，{}-{}-well{}_zid{}.mp4'.format(
        safe_filename(patient_given_names),
        safe_filename(patient_name),
        safe_filename(session_uuid),
        safe_filename(well_no),
        safe_filename(zid),
    )


def download_one_video(client, patient_given_names, patient_name, session_uuid, well_no, zid,
                       output_dir, overwrite, summary, progress):
    filename = make_video_filename(patient_given_names, patient_name, session_uuid, well_no, zid)
    output_path = os.path.join(output_dir, filename)
    try:
        result = client.download_video(session_uuid, well_no, zid, output_path, overwrite=overwrite)
        summary[result] += 1
        progress('info', '{} {}'.format('已跳过' if result == 'skipped' else '已下载', output_path))
    except Exception as ex:
        summary['failed'] += 1
        progress('error', '下载失败: {} {} session_uuid={} well{} zid{}: {}'.format(
            patient_given_names, patient_name, session_uuid, well_no, zid, ex))


def download_patient_videos(client, input_path, output_dir, overwrite=False,
                            progress_callback=None, row_callback=None):
    def progress(level, message):
        if progress_callback:
            progress_callback(level, message)

    check_output_dir_writable(output_dir)

    targets = read_targets(input_path)
    summary = {'downloaded': 0, 'skipped': 0, 'not_found': 0, 'no_session': 0, 'failed': 0}
    total = len(targets)
    rows_without_session_uuid = [target for target in targets if not (target.get('session_uuid') or '').strip()]
    dishrecords = None

    if rows_without_session_uuid:
        progress('info', '正在获取 dishrecords...')
        dishrecords = index_dishrecords(client.get_dishrecords())

    for index, target in enumerate(targets, start=1):
        if row_callback:
            row_callback(index - 1, total)

        patient_given_names = target.get('patient_given_names')
        patient_name = target.get('patient_name')
        well_no = parse_well_no(target.get('no'))
        session_uuid = (target.get('session_uuid') or '').strip()

        if session_uuid:
            for zid in VIDEO_ZIDS:
                download_one_video(client, patient_given_names, patient_name, session_uuid, well_no, zid,
                                   output_dir, overwrite, summary, progress)
            if row_callback:
                row_callback(index, total)
            continue

        key = make_patient_key(patient_given_names, patient_name)
        matches = dishrecords.get(key, [])

        if not matches:
            summary['not_found'] += 1
            progress('warning', '当前服务器未找到 dish，已跳过: {} {} well{}'.format(
                patient_given_names, patient_name, well_no))
            if row_callback:
                row_callback(index, total)
            continue

        for dish in matches:
            dish_uuid = dish.get('dish_uuid')
            sessions = client.get_sessionrecords(dish_uuid)
            if not sessions:
                summary['no_session'] += 1
                progress('warning', '当前服务器未找到 session，已跳过: {} {} dish_uuid={}'.format(
                    patient_given_names, patient_name, dish_uuid))
                continue

            for session in sessions:
                session_uuid = session.get('session_uuid')
                if not session_uuid:
                    summary['no_session'] += 1
                    progress('warning', 'sessionrecord 缺少 session_uuid，已跳过: {} {} dish_uuid={}'.format(
                        patient_given_names, patient_name, dish_uuid))
                    continue
                for zid in VIDEO_ZIDS:
                    download_one_video(client, patient_given_names, patient_name, session_uuid, well_no, zid,
                                       output_dir, overwrite, summary, progress)

        if row_callback:
            row_callback(index, total)

    return summary


class DownloadPatientVideosApp:

    def __init__(self, root):
        self.root = root
        self.root.title('患者视频下载工具')
        self.root.geometry('760x560')
        self.events = queue.Queue()
        self.worker = None

        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar(value=os.path.abspath('videos'))
        self.server = tk.StringVar(value='https://')
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.overwrite = tk.BooleanVar(value=False)
        self.progress_text = tk.StringVar(value='请选择 Excel 文件并填写服务器信息')

        self._build_ui()
        self.root.after(100, self._process_events)

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(9, weight=1)

        ttk.Label(frame, text='Excel 文件').grid(row=0, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.input_path).grid(row=0, column=1, sticky=tk.EW, pady=4)
        ttk.Button(frame, text='选择...', command=self._browse_input).grid(row=0, column=2, padx=(6, 0), pady=4)

        ttk.Label(frame, text='保存目录').grid(row=1, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.output_dir).grid(row=1, column=1, sticky=tk.EW, pady=4)
        ttk.Button(frame, text='选择...', command=self._browse_output_dir).grid(row=1, column=2, padx=(6, 0), pady=4)

        ttk.Label(frame, text='服务器 IP/地址').grid(row=2, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.server).grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=4)

        ttk.Label(frame, text='登录用户名').grid(row=3, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.username).grid(row=3, column=1, columnspan=2, sticky=tk.EW, pady=4)

        ttk.Label(frame, text='登录密码').grid(row=4, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.password, show='*').grid(row=4, column=1, columnspan=2, sticky=tk.EW, pady=4)

        options = ttk.Frame(frame)
        options.grid(row=5, column=1, columnspan=2, sticky=tk.W, pady=4)
        ttk.Checkbutton(options, text='覆盖已存在视频', variable=self.overwrite).pack(side=tk.LEFT)

        self.start_button = ttk.Button(frame, text='预检并开始下载', command=self._start_download)
        self.start_button.grid(row=6, column=0, columnspan=3, sticky=tk.EW, pady=(12, 6))

        self.progress_bar = ttk.Progressbar(frame, mode='determinate')
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky=tk.EW)
        ttk.Label(frame, textvariable=self.progress_text).grid(row=8, column=0, columnspan=3, sticky=tk.NW, pady=(6, 0))

        log_frame = ttk.Frame(frame)
        log_frame.grid(row=9, column=0, columnspan=3, sticky=tk.NSEW, pady=(28, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, height=16, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def _browse_input(self):
        filename = filedialog.askopenfilename(
            title='选择患者 Excel/CSV 文件',
            filetypes=[('Excel/CSV files', '*.xlsx *.xlsm *.csv'), ('Excel files', '*.xlsx *.xlsm'),
                       ('CSV files', '*.csv'), ('All files', '*.*')])
        if filename:
            self.input_path.set(filename)

    def _browse_output_dir(self):
        dirname = filedialog.askdirectory(title='选择视频保存目录')
        if dirname:
            self.output_dir.set(dirname)

    def _validate_inputs(self):
        input_path = self.input_path.get().strip()
        output_dir = self.output_dir.get().strip()
        server = self.server.get().strip()
        username = self.username.get().strip()
        password = self.password.get()

        if not input_path:
            raise RuntimeError('请选择 Excel 或 CSV 文件。')
        if not os.path.isfile(input_path):
            raise RuntimeError('文件不存在: {}'.format(input_path))
        if not output_dir:
            raise RuntimeError('请选择视频保存目录。')
        if not (server.startswith('https://') or server.startswith('http://')):
            raise RuntimeError('服务器地址必须以 http:// 或 https:// 开头。')
        if not username:
            raise RuntimeError('请输入登录用户名。')
        if not password:
            raise RuntimeError('请输入登录密码。')

        check_output_dir_writable(output_dir)
        targets = read_targets(input_path)
        self._append_log('INFO', '预检通过：Excel 表头和数据正常，共 {} 行。'.format(len(targets)))
        self._append_log('INFO', '预检通过：视频保存目录可以写入。')
        self._append_log('INFO', '正在预检 IP、用户名和密码...')
        client = CandlePublicClient(server, username, password)
        self._append_log('INFO', '预检通过：IP 可以连接，用户名和密码可以获取 auth。')
        return input_path, output_dir, server, client

    def _start_download(self):
        if self.worker and self.worker.is_alive():
            return

        self._clear_log()
        self.progress_bar['value'] = 0
        self.progress_text.set('正在预检...')

        try:
            input_path, output_dir, server, client = self._validate_inputs()
        except Exception as ex:
            self.progress_text.set('预检失败')
            messagebox.showerror('预检失败', str(ex))
            return

        self.progress_text.set('开始下载...')
        self.start_button.configure(state=tk.DISABLED)

        args = {
            'input_path': input_path,
            'output_dir': output_dir,
            'server': server,
            'overwrite': self.overwrite.get(),
            'client': client,
        }
        self.worker = threading.Thread(target=self._download_worker, kwargs=args, daemon=True)
        self.worker.start()

    def _download_worker(self, input_path, output_dir, server, overwrite, client):
        try:
            self.events.put(('log', 'INFO', '开始下载，服务器 {}'.format(server)))

            def progress_callback(level, message):
                self.events.put(('log', level.upper(), message))

            def row_callback(current, total):
                self.events.put(('progress', current, total))

            summary = download_patient_videos(
                client,
                input_path,
                output_dir,
                overwrite=overwrite,
                progress_callback=progress_callback,
                row_callback=row_callback,
            )
            self.events.put(('done', summary))
        except Exception as ex:
            self.events.put(('failed', str(ex)))

    def _process_events(self):
        try:
            while True:
                event = self.events.get_nowait()
                event_type = event[0]
                if event_type == 'log':
                    self._append_log(event[1], event[2])
                elif event_type == 'progress':
                    current, total = event[1], event[2]
                    self.progress_bar['maximum'] = total or 1
                    self.progress_bar['value'] = current
                    self.progress_text.set('已处理 {} / {}'.format(current, total))
                elif event_type == 'done':
                    self._finish(event[1])
                elif event_type == 'failed':
                    self._fail(event[1])
        except queue.Empty:
            pass
        self.root.after(100, self._process_events)

    def _append_log(self, level, message):
        self.log_text.insert(tk.END, '[{}] {}\n'.format(level, message))
        self.log_text.see(tk.END)

    def _clear_log(self):
        self.log_text.delete('1.0', tk.END)

    def _finish(self, summary):
        self.start_button.configure(state=tk.NORMAL)
        self.progress_text.set('下载完成')
        text = json.dumps(summary, sort_keys=True, ensure_ascii=False)
        self._append_log('INFO', 'Summary: {}'.format(text))
        messagebox.showinfo('下载完成', '统计结果:\n{}'.format(text))

    def _fail(self, message):
        self.start_button.configure(state=tk.NORMAL)
        self.progress_text.set('下载失败')
        self._append_log('ERROR', message)
        messagebox.showerror('下载失败', message)


def main():
    requests.packages.urllib3.disable_warnings()
    root = tk.Tk()
    app = DownloadPatientVideosApp(root)
    root.mainloop()
    return app


if __name__ == '__main__':
    main()
