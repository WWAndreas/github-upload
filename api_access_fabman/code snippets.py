#add SAP Number
#put Data!

for member in memberList:
    if member.id==221185:
        temp=member.dataset
        temp["metadata"]["SAP"]="654721"
        jsondata=json.dumps(temp)
        url=str("https://fabman.io/api/v1/members/"+str(member.id))
        print(jsondata)
        result = s.put(url, data=jsondata)
        while result.status_code== 429:
            time.sleep(2)
            result = s.put(url, data=jsondata)
        print(result)
        time.sleep(500)

#get All Member Data
#store List in Member Object for further processing
#get List of Active Members
response=s.get("https://fabman.io/api/v1/members", params=member_params)
member_data=response.json()
memberList=[]
originalList=[]
for item in member_data:
     #member = fablab_member.Member(item["id"], item["firstName"],item["lastName"])
    member=fablab_member.Member(item["id"],item["firstName"], item["lastName"])
    member.add_email(item["emailAddress"])
    member.add_dataset(item)
    originalList.append(item)
    if item["lastName"]=="Perfler":
        sap=""
        try:
            sap=item["metadata"]["SAP"]
        except:
            sap="-1"
        member.add_sap((sap))
    memberList.append(member)