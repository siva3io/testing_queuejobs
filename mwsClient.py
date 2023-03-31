from mws import Reports
from mws import Products
import json,pprint
import time
import sys
def request_report():
    print("in RequestReport")
    reports=Reports(access_key="AKIAJKBEW6TOLJHI6AQQ",
             secret_key="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",
             account_id="AYMTXQHS9DXNN",
             auth_token="amzn.mws.5ab4779a-df90-d333-6a38-f1e57e2fab59")
    res=reports.request_report(report_type="_GET_MERCHANT_LISTINGS_ALL_DATA_")
    res_content = res.parsed
    return res_content['ReportRequestInfo']['ReportRequestId']['value']
def getReportRequestList(reportRequestId):
    print("in GetReportRequestList")
    reports=Reports(access_key="AKIAJKBEW6TOLJHI6AQQ",
             secret_key="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",
             account_id="AYMTXQHS9DXNN",
             auth_token="amzn.mws.5ab4779a-df90-d333-6a38-f1e57e2fab59")
    flag = True
    return res_content['ReportRequestInfo']['GeneratedReportId']['value']
def getReport(reportId):
    # reports=Reports(access_key="AKIAJKBEW6TOLJHI6AQQ",
    #          secret_key="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",
    #          account_id="AYMTXQHS9DXNN",
    #          auth_token="amzn.mws.5ab4779a-df90-d333-6a38-f1e57e2fab59")
    # res = reports.get_report(report_id= reportId)
                    
    fname="kkk.txt"
    # txt = open(fname, "wb")
    # txt.write(res.parsed)
    # txt.close()
    fd = open(fname, "r+")
    lines = fd.readlines()
    fd.close()
    l = []
    d = {}
    # asin = []
    asin={}
    for i in range(0, len(l)):
        # asin.append(l[i]['asin1'])
        # asin.append({"ASIN":l[i]['asin1'],"sku_id":l[i]['seller-sku']})
        asin[l[i]['asin1']] = {}
        asin[l[i]['asin1']]["sku_id"] = l[i]['seller-sku']
        asin[l[i]['asin1']]["image_1"] = l[i]['image-url']
        asin[l[i]['asin1']]["product_description"]=l[i]['item-description']
        asin[l[i]['asin1']]['inventory_quantity']=l[i]['quantity']
        asin[l[i]['asin1']]['lp']=l[i]['price']        
    return asin
def getProductWithASIN(asinsku):
    products=Products(access_key="AKIAJKBEW6TOLJHI6AQQ",
             secret_key="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",
             account_id="AYMTXQHS9DXNN",
             auth_token="amzn.mws.5ab4779a-df90-d333-6a38-f1e57e2fab59")
    prev_asins = 0
    ProductList = []
    start = time.time()
    asin=[]
    asin=list(asinsku.keys())
    flag = True
    count = len(asin)
    print(count)
    no_of_asins = 10
    next_asins = 0 + no_of_asins
    prev = 0
    fname="productjson1.txt"
    starttime = time.time()
    for i in range(0, len(asin)+1, 5):#len(asin)+1
        if (i == 0):
            continue
        print({"prev": prev, "next": i, "cont": count})
        try:
            res = products.get_matching_product_for_id(marketplaceid='ATVPDKIKX0DER',type_="ASIN", ids=asin[prev:i])
            # ProductList.extend(res.parsed)
            # catres=products.get_product_categories_for_asin(marketplaceid='ATVPDKIKX0DER', asin=asin[i:i + count % 5])

            res = list(res.parsed)
            with open(fname, 'a+') as f:
                for item in res:
                    catres = None
                    itemDict = dict(item)
                    itemDict['description'] = asinsku[item['Id']['value']]
                    f.write("%s\n" % itemDict)
            time.sleep(70)
        except Exception as e:
            print("Exception Raised---------->", e.args, "---->")
            print('Error on line {}--->56 '.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e))
            time.sleep(1)
            prev = i
            continue
        prev = i
        if prev == 1000:
            time.sleep(36000-(time.time()-startTime))
            starttime = time.time()

    if (len(asin) % 5 == 0):
        pass
    else:
        try:
            print({"prev": i, "next": i + count % 10, "cont": count})
            res=products.get_matching_product_for_id(marketplaceid='ATVPDKIKX0DER',type_="ASIN", ids=asin[i:i + count % 5])
            # res = p.get_matching_product("ATVPDKIKX0DER", asin[i:i + count % 10])
            # catres=products.get_product_category_for_ASIN(marketplaceid='ATVPDKIKX0DER', asin=asin[i:i + count % 5])
            ProductList.extend(res.parsed)
            with open(fname, 'a+') as f:
                for item in res:
                    catres = None
                    itemDict = dict(item)
                    itemDict['description'] = asinsku[item['Id']['value']]
                    if prev%30!=0:
                        catres=products.get_product_categories_for_asin(marketplaceid='ATVPDKIKX0DER', asin=item['Id']['value'])
                    else:
                        catres=products.get_product_categories_for_sku(marketplaceid='ATVPDKIKX0DER', sku = itemDict['description']['sku_id'])
                    itemDict['categoryDescription'] = dict(catres.parsed)
                    f.write("%s\n" % itemDict)

        except Exception as e:
            print("Exception Raised---------->", e.args)
            print('Error on line {}--->71 '.format(sys.exc_info()[-1].tb_lineno) + str(type(e).__name__) + str(e))
    end = time.time()
    print(end-start)
    print('complete')
s=getReport('16549088718018149')
print("get report completed")
getProductWithASIN(s)
