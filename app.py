from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from config import load_config, dump_config, upgrade_settings

# Load configuration
cfg = load_config()

# Ensure the configuration is upgraded if necessary
base_config = {
    'PLEX_SERVER': os.getenv('PLEX_URL', 'https://plex.your-server.com'),
    'PLEX_TOKEN': os.getenv('PLEX_TOKEN', ''),
    'PLEX_LIBRARIES': os.getenv('PLEX_LIBRARIES', '').split(',') if os.getenv('PLEX_LIBRARIES') else [],
    'AUDIO_CODEC_SCORES': {'Unknown': 0, 'wmapro': 200, 'mp2': 500, 'mp3': 1000, 'ac3': 1000, 'dca': 2000, 'pcm': 2500,
                           'flac': 2500, 'dca-ma': 4000, 'truehd': 4500, 'aac': 1000, 'eac3': 1250},
    'VIDEO_CODEC_SCORES': {'Unknown': 0, 'h264': 10000, 'h265': 5000, 'hevc': 5000, 'mpeg4': 500, 'vc1': 3000,
                           'vp9': 1000, 'mpeg1video': 250, 'mpeg2video': 250, 'wmv2': 250, 'wmv3': 250, 'msmpeg4': 100,
                           'msmpeg4v2': 100, 'msmpeg4v3': 100},
    'VIDEO_RESOLUTION_SCORES': {'Unknown': 0, '4k': 20000, '1080': 10000, '720': 5000, '480': 3000, 'sd': 1000},
    'FILENAME_SCORES': {},
    'SKIP_LIST': os.getenv('SKIP_LIST', '').split(',') if os.getenv('SKIP_LIST') else [],
    'SCORE_FILESIZE': os.getenv('SCORE_FILESIZE', 'true').lower() == 'true',
    'AUTO_DELETE': os.getenv('AUTO_DELETE', 'false').lower() == 'true',
    'FIND_DUPLICATE_FILEPATHS_ONLY': os.getenv('FIND_DUPLICATE_FILEPATHS_ONLY', 'false').lower() == 'true'
}

upgraded, cfg = upgrade_settings(base_config, cfg)
if upgraded:
    dump_config(cfg)

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
        dump_config(cfg)
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
    if title in process_later:
        for part_id, part in process_later[title].items():
            if part_id != media_id:
                delete_item(part.key, part_id)
                write_decision(removed=part)
        write_decision(keeping=media_id)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
