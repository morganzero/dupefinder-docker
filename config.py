import json
import os
import sys

from attrdict import AttrDict
from plexapi.myplex import MyPlexAccount
from getpass import getpass

config_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'config.json')
base_config = {
    'PLEX_SERVER': os.getenv('PLEX_SERVER', 'https://plex.your-server.com'),
    'PLEX_TOKEN': os.getenv('PLEX_TOKEN', ''),
    'PLEX_LIBRARIES': os.getenv('PLEX_LIBRARIES', '').split(','),
    'AUDIO_CODEC_SCORES': {'Unknown': 0, 'wmapro': 200, 'mp2': 500, 'mp3': 1000, 'ac3': 1000, 'dca': 2000, 'pcm': 2500,
                           'flac': 2500, 'dca-ma': 4000, 'truehd': 4500, 'aac': 1000, 'eac3': 1250},
    'VIDEO_CODEC_SCORES': {'Unknown': 0, 'h264': 10000, 'h265': 5000, 'hevc': 5000, 'mpeg4': 500, 'vc1': 3000,
                           'vp9': 1000, 'mpeg1video': 250, 'mpeg2video': 250, 'wmv2': 250, 'wmv3': 250, 'msmpeg4': 100,
                           'msmpeg4v2': 100, 'msmpeg4v3': 100},
    'VIDEO_RESOLUTION_SCORES': {'Unknown': 0, '4k': 20000, '1080': 10000, '720': 5000, '480': 3000, 'sd': 1000},
    'FILENAME_SCORES': {},
    'SKIP_LIST': os.getenv('SKIP_LIST', '').split(','),
    'SCORE_FILESIZE': os.getenv('SCORE_FILESIZE', 'true').lower() == 'true',
    'AUTO_DELETE': os.getenv('AUTO_DELETE', 'false').lower() == 'false',
    'FIND_DUPLICATE_FILEPATHS_ONLY': os.getenv('FIND_DUPLICATE_FILEPATHS_ONLY', 'false').lower() == 'false'
}
cfg = None


class AttrConfig(AttrDict):
    """
    Simple AttrDict subclass to return None when requested attribute does not exist
    """

    def __init__(self, config):
        super().__init__(config)

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            pass
        # Default behaviour
        return None


def prefilled_default_config(configs):
    default_config = base_config.copy()
    return default_config


def build_config():
    if not os.path.exists(config_path):
        print("Dumping default config to: %s" % config_path)
        with open(config_path, 'w') as fp:
            json.dump(prefilled_default_config({}), fp, sort_keys=True, indent=2)
        return True
    else:
        return False


def dump_config():
    if os.path.exists(config_path):
        with open(config_path, 'w') as fp:
            json.dump(cfg, fp, sort_keys=True, indent=2)
        return True
    else:
        return False


def load_config():
    with open(config_path, 'r') as fp:
        return AttrConfig(json.load(fp))


def upgrade_settings(defaults, currents):
    upgraded = False

    def inner_upgrade(default, current, key=None):
        sub_upgraded = False
        merged = current.copy()
        if isinstance(default, dict):
            for k, v in default.items():
                # missing k
                if k not in current:
                    merged[k] = v
                    sub_upgraded = True
                    if not key:
                        print("Added %r config option: %s" % (str(k), str(v)))
                    else:
                        print("Added %r to config option %r: %s" % (str(k), str(key), str(v)))
                    continue
                # iterate children
                if isinstance(v, dict) or isinstance(v, list):
                    did_upgrade, merged[k] = inner_upgrade(default[k], current[k], key=k)
                    sub_upgraded = did_upgrade if did_upgrade else sub_upgraded

        elif isinstance(default, list) and key:
            for v in default:
                if v not in current:
                    merged.append(v)
                    sub_upgraded = True
                    print("Added to config option %r: %s" % (str(key), str(v)))
                    continue
        return sub_upgraded, merged

    upgraded, upgraded_settings = inner_upgrade(defaults, currents)
    return upgraded, AttrConfig(upgraded_settings)


############################################################
# LOAD CFG
############################################################

# dump/load config
if build_config():
    print("Please edit the default configuration before running again!")
    sys.exit(0)
else:
    tmp = load_config()
    upgraded, cfg = upgrade_settings(base_config, tmp)
    if upgraded:
        dump_config()
        print("New config options were added, adjust and restart!")
        sys.exit(0)