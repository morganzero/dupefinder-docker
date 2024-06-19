import json
import os
import sys

from attrdict import AttrDict
from plexapi.myplex import MyPlexAccount
from getpass import getpass

config_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'config.json')

def replace_placeholders(config):
    plex_url = os.getenv('PLEX_URL', 'https://plex.your-server.com')
    plex_token = os.getenv('PLEX_TOKEN', '')
    
    config['PLEX_SERVER'] = plex_url
    config['PLEX_TOKEN'] = plex_token

    return config

def load_config():
    if not os.path.exists(config_path):
        return create_default_config()
    
    try:
        with open(config_path, 'r') as fp:
            config = json.load(fp)
        config = replace_placeholders(config)
        return AttrConfig(config)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error loading config.json. Creating a new default config.")
        return create_default_config()

def create_default_config():
    default_config = {
        "SCORE_FILESIZE": True,
        "AUTO_DELETE": False,
        "FIND_DUPLICATE_FILEPATHS_ONLY": False,
        "PLEX_SERVER": os.getenv('PLEX_URL', 'https://plex.your-server.com'),
        "PLEX_TOKEN": os.getenv('PLEX_TOKEN', ''),
        "PLEX_LIBRARIES": [],
        "SKIP_LIST": [
            "/Plex Versions/"
        ],
        "AUDIO_CODEC_SCORES": {
            "Unknown": 0,
            "aac": 5000,
            "ac3": 4500,
            "dca": 2000,
            "dca-ma": 4000,
            "eac3": 1250,
            "flac": 4000,
            "mp2": 500,
            "mp3": 1000,
            "pcm": 2500,
            "truehd": 0,
            "wmapro": 0
        },
        "FILENAME_SCORES": {
            "*.avi": -1000,
            "*.ts": -1000,
            "*.vob": -5000,
            "*1080p*BluRay*": 15000,
            "*720p*BluRay*": 10000,
            "*HDTV*": -1000,
            "*PROPER*": 1500,
            "*REPACK*": 1500,
            "*Remux*": 20000,
            "*WEB*CasStudio*": 5000,
            "*WEB*KINGS*": 5000,
            "*WEB*NTB*": 5000,
            "*WEB*QOQ*": 5000,
            "*WEB*SiGMA*": 5000,
            "*WEB*TBS*": -1000,
            "*WEB*TROLLHD*": 2500,
            "*WEB*VISUM*": 5000,
            "*dvd*": -1000,
            "*deflate*": 10000,
            "*inflate*": 10000,
            "*AJP69*": 10000,
            "*BTN*": 10000,
            "*CasStudio*": 10000,
            "*CtrlHD*": 10000,
            "*KiNGS*": 10000,
            "*monkee*": 10000,
            "*NTb*": 10000,
            "*NTG*": 10000,
            "*QOQ*": 10000,
            "*RTN*": 10000,
            "*FLUX*": 10000,
            "*TOMMY*": 10000,
            "*ViSUM*": 10000,
            "*T6D*": 10000,
            "*RAPiDCOWS*": 10000,
            "*BTW*": 10000,
            "*Chotab*": 10000,
            "*CiT*": 10000,
            "*DEEP*": 10000,
            "*iJP*": 10000,
            "*iT00NZ*": 10000,
            "*LAZY*": 10000,
            "*NYH*": 10000,
            "*SA89*": 10000,
            "*SIGMA*": 10000,
            "*TEPES*": 10000,
            "*TVSmash*": 10000,
            "*SDCC*": 10000,
            "*iKA*": 10000,
            "*iJP*": 10000,
            "*Cinefeel*": 10000,
            "*SPiRiT*": 10000,
            "*FC*": 10000,
            "*JETIX*": 10000,
            "*Coo7*": 10000,
            "*WELP*": 10000,
            "*KiMCHI*": 10000,
            "*BLUTONiUM*": 10000,
            "*orbitron*": 10000,
            "*ETHiCS*": 10000,
            "*RTFM*": 10000,
            "*PSiG*": 10000,
            "*MZABI*": 10000,
            "*BMF*": 10000,
            "*decibeL*": 10000,
            "*D-Z0N3*": 10000,
            "*FTW-HD*": 10000,
            "*HiFi*": 10000,
            "*NCmt*": 10000,
            "*OISTiLe*": 10000,
            "*TDD*": 10000,
            "*ZQ*": 10000,
            "*HiSD*": 10000,
            "*NTb*": 10000,
            "*ift*": 10000,
            "*geek*": 10000,
            "*tnp*": 10000,
            "*ncmt*": 10000,
            "*pter*": 10000,
            "*bbq*": 10000,
            "*CRiSC*": 10000,
            "*CtrlHD*": 10000,
            "*DON*": 10000,
            "*EA*": 10000,
            "*EbP*": 10000,
            "*LolHD*": 10000,
            "*SbR*": 10000,
            "*TayTo*": 10000,
            "*VietHD*": 10000,
            "*BHDStudio*": 10000,
            "*FraMeSToR*": 10000,
            "*EPSiLON*": 10000,
            "*KRaLiMaRKo*": 10000,
            "*PmP*": 10000,
            "*BLURANiUM*": 10000,
            "*SiCFoI*": 10000,
            "*SURFINBIRD*": 10000,
            "*GalaxyGR*": -20000,
            "*TGx*": -20000,
            "*SPARKS*": -20000,
            "*RARBG*": -20000,
            "*aXXo*": -20000,
            "*CrEwSaDe*": -20000,
            "*DNL*": -20000,
            "*FaNGDiNG0*": -20000,
            "*FRDS*": -20000,
            "*HDTime*": -20000,
            "*iPlanet*": -20000,
            "*KiNGDOM*": -20000,
            "*Leffe*": -20000,
            "*mHD*": -20000,
            "*mSD*": -20000,
            "*nHD*": -20000,
            "*nikt0*": -20000,
            "*nSD*": -20000,
            "*NhaNc3*": -20000,
            "*PRODJi*": -20000,
            "*RDN*": -20000,
            "*SANTi*": -20000,
            "*STUTTERSHIT*": -20000,
            "*WAF*": -20000,
            "*x0r*": -20000,
            "*YIFY*": -20000,
            "*YTS*": -20000,
            "*FGT*": -20000,
            "*d3g*": -20000,
            "*MeGusta*": -20000,
            "*tigole*": -20000,
            "*C4K*": -20000,
            "*RARBG*": -20000,
            "*4K4U*": -20000,
            "*AROMA*": -20000,
            "*CrEwSaDe*": -20000,
            "*HDTime*": -20000,
            "*iPlanet*": -20000,
            "*NhaNc3*": -20000,
            "*LiGaS*": -20000,
            "*DDR*": -20000,
            "*Zeus*": -20000,
            "*Tigole*": -20000,
            "*TBS*": -20000,
            "*beAst*": -20000,
            "*CHD*": -20000,
            "*HDWinG*": -20000,
            "*MTeam*": -20000,
            "*MySiLU*": -20000,
            "*WiKi*": -20000,
            "*Rifftrax*": -20000,
            "*RU4HD*": -20000,
            "*GalaxyTV*": -20000,
            "*TF1*": -20000,
            "*Telly*": -20000,
            "*rartv*": -20000,
            "*eztv*": -20000,
            "*TGx*": -20000,
            "*4P*": -20000,
            "*4Planet*": -20000,
            "*BUYMORE*": -20000,
            "*Chamele0n*": -20000,
            "*GEROV*": -20000,
            "*iNC0GNiTO*": -20000,
            "*NZBGeek*": -20000,
            "*Obfuscated*": -20000,
            "*postbot*": -20000,
            "*Rakuv*": -20000,
            "*Scrambled*": -20000,
            "*WhiteRev*": -20000,
            "*VIDEOHOLE*": -20000,
            "*TBS*": -20000,
            "*BRiNK*": -20000,
            "*CHX*": -20000,
            "*XLF*": -20000,
            "*worldmkv*": -20000,
            "*GHOSTS*": -20000,
            "*WEB*HorribleSubs*": 5000,
            "*WEB*AnimeGR*": 5000,
            "*WEB*Erai*": 5000,
            "*WEB*raws*": 5000,
            "*Dual*": 40000,
            "*Dual-Audio*": 40000,
            "*JA+EN*": 30000,
            "*Eng-Subs*": 35000,
            "*Subs*":  25000
        },
        "VIDEO_CODEC_SCORES": {
            "Unknown": 0,
            "h264": 10000,
            "h265": 5000,
            "hevc": 5000,
            "mpeg1video": 250,
            "mpeg2video": 250,
            "mpeg4": 500,
            "msmpeg4": 100,
            "msmpeg4v2": 100,
            "msmpeg4v3": 100,
            "vc1": 3000,
            "vp9": 1000,
            "wmv2": 250,
            "wmv3": 250
        },
        "VIDEO_RESOLUTION_SCORES": {
            "1080": 10000,
            "480": 3000,
            "4k": 0,
            "720": 5000,
            "Unknown": 0,
            "sd": 1000
        }
    }
    dump_config(AttrConfig(default_config))
    return AttrConfig(default_config)

def dump_config(cfg):
    with open(config_path, 'w') as fp:
        json.dump(cfg, fp, sort_keys=True, indent=2)
    return True

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
                        print(f"Added {k!r} config option: {v!r}")
                    else:
                        print(f"Added {k!r} to config option {key!r}: {v!r}")
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
                    print(f"Added to config option {key!r}: {v!r}")
                    continue
        return sub_upgraded, merged

    upgraded, upgraded_settings = inner_upgrade(defaults, currents)
    return upgraded, AttrConfig(upgraded_settings)


############################################################
# LOAD CFG
############################################################

cfg = load_config()
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
    print("New config options were added. The configuration has been updated and the script will continue execution.")
