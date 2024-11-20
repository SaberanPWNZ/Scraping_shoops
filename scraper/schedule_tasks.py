from celery.schedules import crontab

from stores.KTC.tasks import start_ktc_wacom, start_ktc_xp_pen


beat = {
    # ROZETKA
    # 'start_rozetka_wacom_every_hour_wacom': {
    #     'task': 'stores.Rozetka.rozetka.start_rozetka_wacom',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    #     'args': ('https://rozetka.com.ua/search/?producer=wacom&redirected=1&seller=rozetka&text=wacom',)
    # },
    # 'start_rozetka_xp_pen_every_hour': {
    #     'task': 'stores.Rozetka.rozetka.start_rozetka_xp_pen',
    #     'schedule':crontab(minute=f'*/{updating_time}'),
    #     'args': (
    #         'https://rozetka.com.ua/ua/search/?producer=xp-pen&redirected=1&section_id=83199&seller=rozetka&text=xp+pen',)
    # },
    # 'start_brain_wacom_every_hour': {
    #     'task': 'stores.Brain.brain.start_brain_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_brain_xp_pen_every_hour': {
    #     'task': 'stores.Brain.brain.start_brain_xp_pen',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_citrus_wacom_every_hour': {
    #     'task': 'stores.Citrus.citrus.start_citrus_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_click_wacom_every_hour': {
    #     'task': 'stores.Click.click.start_click_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_click_xp_pen_every_hour': {
    #     'task': 'stores.Click.click.start_click_xp_pen',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_wacomstore_every_hour': {
    #     'task': 'stores.WacomStore.wacom_store.start_wacom_store_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # MOYO
    # 'start_moyo_wacom_every_hour': {
    #     'task': 'stores.Moyo.moyo.start_moyo',
    #     'schedule': crontab(minute='*/3'),
    # },
    # # AUCHAN
    # 'start_auchan_wacom_every_hour': {
    #     'task': 'stores.Auchan.auchan.start_auchan_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # KTC - xp-pen 2 items do not founded
    'start_ktc_wacom_every_hour': {
        'task': 'stores.KTC.ktc.start_ktc_wacom',
        'schedule': crontab(minute='*'),
    },
    'start_ktc_xp_pen_every_hour': {
        'task': 'stores.KTC.ktc.start_ktc_xp_pen',
        'schedule': crontab(minute='*'),
    }#,
    # # Foxtrot
    # 'start_foxtrot_wacom_every_hour': {
    #     'task': 'stores.Foxtrot.foxtrot.start_foxtrot_wacom',
    #     'schedule': crontab(minute='*/3'),
    },
    # 'start_foxtrot_xp_pen_every_hour': {
    #     'task': 'stores.WO.Wo.start_wo_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_wo_wacom_every_hour': {
    #     'task': 'stores.WO.Wo.start_wo_xp_pen',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_wo_xp_pen_every_hour': {
    #     'task': 'stores.Foxtrot.foxtrot.start_foxtrot_xp_pen',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_setevuha_every_hour': {
    #     'task': 'stores.Setevuha.setevuha.start_setevuha',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_can_wacom_every_hour': {
    #     'task': 'stores.CAN.can.start_can_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_can_xp_every_hour': {
    #     'task': 'stores.CAN.can.start_can_xp_pen',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_comtrading_wacom_every_hour': {
    #     'task': 'stores.Comtrading.comtrading.start_comtrading_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_comtrading_xp_pen_every_hour': {
    #     'task': 'stores.Comtrading.comtrading.start_comtrading_xp_pen',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_exe_wacom_every_hour': {
    #     'task': 'stores.EXE.exe.start_exe_wacom',
    #     'schedule': crontab(minute='*/3'),
    # },
    # 'start_exe_xp_pen_every_hour': {
    #     'task': 'stores.EXE.exe.start_exe_xp_pen',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # # },
    # 'start_fotos_wacom_every_hour': {
    #     'task': 'stores.F.fotos.start_fotos',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # },
    #
    # 'start_fotos_xp_pen_every_hour': {
    #     'task': 'stores.F.fotos.start_fotos_xp_pen',
    #     'schedule':crontab(minute=f'*/{updating_time}'),
    # },
    # 'start_itbox_wacom_every_hour': {
    #     'task': 'stores.Itbox.itbox.start_itbox_wacom',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # },
    # 'start_itbox_xp_pen_every_hour': {
    #     'task': 'stores.Itbox.itbox.start_itbox_xp_pen',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # },
    # 'start_mta_wacom_every_hour': {
    #     'task': 'stores.MTA.mta.start_mta',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # },
    # 'start_portativ_wacom_every_hour': {
    #     'task': 'stores.Portativ.portativ.start_portativ_wacom',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # },
    # 'start_portativ_xp_pen_every_hour': {
    #     'task': 'stores.Portativ.portativ.start_portativ_xp_pen',
    #     'schedule': crontab(minute=f'*/{updating_time}'),
    # },
    #
    # 'start_comfy_wacom_every_hour': {
    #     'task': 'stores.Comfy.comfy.start_comfy_wacom',
    #     'schedule': crontab(minute=f'*/5'),
    # },
#     # UPDATE DATABASE
#     'update_database_wacom_every_hour': {
#         'task': 'databases.db_helper.update_db',
#         'schedule': crontab(minute='*/2'),
#         'kwargs': {'table_url': wacom_table_url, 'sheet_name': 'WACOM'}
#     },
#     'update_database_xp_pen_every_hour': {
#         'task': 'databases.db_helper.update_db_xp_pen',
#         'schedule': crontab(minute='*/2'),
#         'kwargs': {'table_url': xp_pen_table_url, 'sheet_name': 'XP-PEN'}
#     },
# }

