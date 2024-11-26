from datetime import datetime
from all.configs._def_main_ import *
from all.functions.func_avs.func_roxy import *



nombregate = "Roxy"
tipogate = "Payflow Avs"
cmdgate = "rx"


@Techie(f'{cmdgate}')
async def roxycmds(_, message):
    tiempo = time.time()
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    usuario = collection.find_one({"_id": message.from_user.id})

    if usuario is None:
        caption = await registrar_usuario(message)
        return await message.reply(text=caption, reply_markup=dbre, quote=True)
    else:
        pass

    if usuario['status'] == "Banned":
        return

    comandos_habilitados = cargar_datos()

    if usuario is not None and usuario.get("role") == "Owner":
        pass
    else:
        if not comandos_habilitados.get('rx', {}).get('enabled', False):
            reason = comandos_habilitados.get(
                'rx', {}).get('reason', "Unknown")
            date = comandos_habilitados.get('rx', {}).get('date', "Unknown")
            _textoff = f"""<b>━━━━━━━━「ELAINA」━━━━━━━━
<i>This command is under maintenance. Please wait until it's fixed.</i> ❗ 
━━━━━━━━「ELAINA」━━━━━━━━</b>"""
            return await message.reply(text=_textoff, quote=True)

    if message.reply_to_message:
        input = getCards(str(message.reply_to_message.text))
    else:
        input = getCards(str(message.text))

    vnnotmsg = f"""<b>━━━━━━━━「ELAINA」━━━━━━━━
<i>Gateways</i> ➣ <i>{nombregate}|{tipogate}</i>
<i>Command</i> ➣ <code>${cmdgate}</code>
<i>Format</i> ➣ <code>${cmdgate} cc|month|year|cvv</code>
━━━━━━━━「ELAINA」━━━━━━━━</b>"""

    if not input:
        return await message.reply(text=vnnotmsg, quote=True)

    grupo = collection_tres.find_one({"group": str(message.chat.id)})

    if usuario['key'] != 'None' or grupo != None:
        if usuario['key'] != 'None':
            if usuario["key"] < datetime.now():
                collection.update_one({"_id": message.from_user.id}, {
                                      "$set": {"key": 'None'}})
                collection.update_one({"_id": message.from_user.id}, {
                                      "$set": {"antispam": 60}})
                collection.update_one({"_id": message.from_user.id}, {
                                      "$set": {"plan": 'Free User'}})
                return await message.reply(text=expiracion, quote=True)
        elif grupo["key"] < datetime.now():
            collection_tres.delete_one({"group": str(message.chat.id)})

    else:
        return await message.reply(text=notpermiso, reply_markup=buypremium, quote=True)
    
    cc = input[0][0]
    mes = input[0][1]
    ano = input[0][2]
    cvv = input[0][3]

    if len(input[0]) > 4:
        estado = input[0][4]
        if estado == "expired":
            return await message.reply(text=expiredmsg, quote=True)
    else:
        estado = None

    vlunh = checkLuhn(cc)

    if vlunh == False:
        return await message.reply(text=noluhn, quote=True)

    if usuario['plan'] == 'Premium':
        max_tareas = 2
    elif usuario['role'] == 'Seller':
        max_tareas = 4
    elif usuario['plan'] == 'Free':
        max_tareas = 1
    elif usuario['plan'] == 'Free User':
        max_tareas = 1
    elif usuario['role'] == 'Owner':
        max_tareas = float('inf')
    else:
        max_tareas = 1

    if max_tareas == 0:
        return

    tareas_en_proceso = usuario.get('tareas_en_proceso', 0)

    if tareas_en_proceso >= max_tareas:
        await Client.send_message(_, chat_id=message.chat.id, text=texto_spam, reply_to_message_id=message.id)
        return

    collection.update_one({"_id": message.from_user.id}, {
                          "$set": {"tareas_en_proceso": tareas_en_proceso + 1}})

    if cc[0] in bin_prohibido:
        collection.update_one({"_id": message.from_user.id}, {
            "$inc": {"tareas_en_proceso": -1}})
        return await message.reply(text=vnnotmsg, quote=True)

    if cc[0] in bin_prohibido:
        collection.update_one({"_id": message.from_user.id}, {
            "$inc": {"tareas_en_proceso": -1}})
        return await message.reply(text=vnnotmsg, quote=True)
    
    x = get_bin_info(cc[0:6])

    baneado = f"""<b><i>Bin Banned</i></b>"""

    bin = cc[:6]

    banned_bins = load_banned_bins()

    if bin in banned_bins:
        collection.update_one({"_id": message.from_user.id}, {
            "$inc": {"tareas_en_proceso": -1}})
        return await message.reply(text=baneado, quote=True)

    if x.get("level") is not None and "PREPAID" in x.get("level"):
        collection.update_one({"_id": message.from_user.id}, {
            "$inc": {"tareas_en_proceso": -1}})

        return await message.reply(text=baneado, quote=True)

    texto_1 = carga1.format(cc=cc, mes=mes, ano=ano, cvv=cvv, brand=x.get("vendor"), level=x.get("level"), typea=x.get("type"),
                            country_flag=x.get("flag"), nombregate=nombregate, ID=ID, FIRST=FIRST, tipogate=tipogate, user_plan=usuario["apodo"])


    
    ñ = await message.reply(text=texto_1, quote=True)
    Status = await Payflowavs(cc, mes, ano, cvv)
    
    if (Status[0] == 'Approved') :
            AVSDATA = Status[2]    
            PROCCVV2 = Status[3]
            RESPMSG = Status[1]
            respstatus = 'Approved 🟩'
            try :
                await ñ.edit(text=f"""<b>
━━━━━━━━「ELAINA」━━━━━━━━
<i>Card</i> ➣ <code>{cc}|{mes}|{ano}|{cvv}</code>
<i>Status</i> ➣ <code>{respstatus} </code>
<i>Result</i> ➣ <i>{RESPMSG}</i>
<i>Cvv</i> [{PROCCVV2}] | <i>Avs</i> [{AVSDATA}]
━━━━━━━━「RESULT」━━━━━━━━
<i>Bank</i> ➣ <code>{x.get("bank_name")}</code>
<i>Country</i> ➣ <code>{x.get("country")} | {x.get("flag")}</code>
<i>Info</i> ➣ <code>{x.get("vendor")} {x.get("level")} {x.get("type")}</code>
━━━━━━━━「INFO」━━━━━━━━━━
<i>Time</i> ➣ <code>{get_time_taken(tiempo)}</code>'s
<i>Gateways</i> ➣ <i>{nombregate}|{tipogate}</i>
<i>Checked by</i> ➣ <a href="tg://user?id={ID}">{FIRST}</a> [<code>{usuario["apodo"]}</code>]
━━━━━━━━「ELAINA」━━━━━━━━</b>""")

                collection.update_one({"_id": message.from_user.id}, {
                            "$inc": {"tareas_en_proceso": -1}})
            except Exception as e:
                print(f"Se produjo una excepción no manejada: {e}")
                return

    elif (Status[0] == 'Declined') :
            AVSDATA = Status[2]
            PROCCVV2 = Status[3]    
            RESPMSG = Status[1]
            respstatus = 'Declined! 🟥'
            try :
                await ñ.edit(text=f"""<b>
━━━━━━━━「ELAINA」━━━━━━━━
<i>Card</i> ➣ <code>{cc}|{mes}|{ano}|{cvv}</code>
<i>Status</i> ➣ <code>{respstatus} </code>
<i>Result</i> ➣ <i>{RESPMSG}</i>
<i>Cvv</i> [{PROCCVV2}] | <i>Avs</i> [{AVSDATA}]
━━━━━━━━「RESULT」━━━━━━━━
<i>Bank</i> ➣ <code>{x.get("bank_name")}</code>
<i>Country</i> ➣ <code>{x.get("country")} | {x.get("flag")}</code>
<i>Info</i> ➣ <code>{x.get("vendor")} {x.get("level")} {x.get("type")}</code>
━━━━━━━━「INFO」━━━━━━━━━━
<i>Time</i> ➣ <code>{get_time_taken(tiempo)}</code>'s
<i>Gateways</i> ➣ <i>{nombregate}|{tipogate}</i>
<i>Checked by</i> ➣ <a href="tg://user?id={ID}">{FIRST}</a> [<code>{usuario["apodo"]}</code>]
━━━━━━━━「ELAINA」━━━━━━━━</b>""")

                collection.update_one({"_id": message.from_user.id}, {
                            "$inc": {"tareas_en_proceso": -1}})
            except Exception as e:
                print(f"Se produjo una excepción no manejada: {e}")
                return
    
    if (Status[0] == 'ApprovedSinCVV') :
            RESPMSG = Status[1]
            respstatus = 'Approved 🟩'
            try :
                await ñ.edit(text=f"""<b>
━━━━━━━━「ELAINA」━━━━━━━━
<i>Card</i> ➣ <code>{cc}|{mes}|{ano}|{cvv}</code>
<i>Status</i> ➣ <code>{respstatus} </code>
<i>Result</i> ➣ <i>{RESPMSG}</i>
━━━━━━━━「RESULT」━━━━━━━━
<i>Bank</i> ➣ <code>{x.get("bank_name")}</code>
<i>Country</i> ➣ <code>{x.get("country")} | {x.get("flag")}</code>
<i>Info</i> ➣ <code>{x.get("vendor")} {x.get("level")} {x.get("type")}</code>
━━━━━━━━「INFO」━━━━━━━━━━
<i>Time</i> ➣ <code>{get_time_taken(tiempo)}</code>'s
<i>Gateways</i> ➣ <i>{nombregate}|{tipogate}</i>
<i>Checked by</i> ➣ <a href="tg://user?id={ID}">{FIRST}</a> [<code>{usuario["apodo"]}</code>]
━━━━━━━━「ELAINA」━━━━━━━━</b>""")

                collection.update_one({"_id": message.from_user.id}, {
                            "$inc": {"tareas_en_proceso": -1}})
            except Exception as e:
                print(f"Se produjo una excepción no manejada: {e}")
                return
        
    elif (Status[0] == 'DeclinedSinCVV') :
            RESPMSG = Status[1]
            respstatus = 'Declined! 🟥'
            try :
                await ñ.edit(text=f"""<b>
━━━━━━━━「ELAINA」━━━━━━━━
<i>Card</i> ➣ <code>{cc}|{mes}|{ano}|{cvv}</code>
<i>Status</i> ➣ <code>{respstatus} </code>
<i>Result</i> ➣ <i>{RESPMSG}</i>
━━━━━━━━「RESULT」━━━━━━━━
<i>Bank</i> ➣ <code>{x.get("bank_name")}</code>
<i>Country</i> ➣ <code>{x.get("country")} | {x.get("flag")}</code>
<i>Info</i> ➣ <code>{x.get("vendor")} {x.get("level")} {x.get("type")}</code>
━━━━━━━━「INFO」━━━━━━━━━━
<i>Time</i> ➣ <code>{get_time_taken(tiempo)}</code>'s
<i>Gateways</i> ➣ <i>{nombregate}|{tipogate}</i>
<i>Checked by</i> ➣ <a href="tg://user?id={ID}">{FIRST}</a> [<code>{usuario["apodo"]}</code>]
━━━━━━━━「ELAINA」━━━━━━━━</b>""")

                collection.update_one({"_id": message.from_user.id}, {
                            "$inc": {"tareas_en_proceso": -1}})
            except Exception as e:
                print(f"Se produjo una excepción no manejada: {e}")
                return
    
    
    
    