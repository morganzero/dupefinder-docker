from flask import Flask, request, jsonify, render_template, redirect, url_for
import subprocess
import os
import json
from config import load_config, cfg, dump_config, upgrade_settings
from dupefinder import get_dupes, delete_item, write_decision, build_tabulated
from tabulate import tabulate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        data = request.form.to_dict()
        cfg.PLEX_SERVER = data.get('PLEX_SERVER')
        cfg.PLEX_TOKEN = data.get('PLEX_TOKEN')
        cfg.AUTO_DELETE = data.get('AUTO_DELETE') == 'on'
        dump_config()
        return redirect(url_for('index'))
    return render_template('config.html', config=cfg)

@app.route('/find_dupes', methods=['GET'])
def find_dupes():
    process_later = {}
    for section in cfg.PLEX_LIBRARIES:
        dupes = get_dupes(section)
        for item in dupes:
            parts = {part.id: part for part in item.media}
            process_later[item.title] = parts
    return render_template('dupes.html', dupes=process_later)

@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    title = data.get('title')
    media_id = data.get('media_id')
    for item in process_later[title]:
        if item.id != media_id:
            delete_item(item.key, item.id)
            write_decision(removed=item)
    write_decision(keeping=media_id)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    if not build_config():
        tmp = load_config()
        upgraded, cfg = upgrade_settings(base_config, tmp)
        if upgraded:
            dump_config()
    app.run(host='0.0.0.0', port=5000)
