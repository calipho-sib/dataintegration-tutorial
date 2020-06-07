import requests, sys, json, os

'''Ensemble REST API'''
server = "https://rest.ensembl.org"

start = sys.argv[1]
end = sys.argv[2]
start = int(start)
end = int(end)

ids = []

counter = 0
with open('ids.txt') as idsfile:
    for line in idsfile:
        if (counter >= (start - 1)):
            line = line.strip('\n')
            id = { "snp" : line.split(',')[0], "ensg" : line.split(',')[1]}
            ids.append(id)

        counter += 1

        if counter > end:
            break

'''Calling REST API'''
json_data = []
for id in ids:
    print("Calling ensembl API for "+str(id))
    ext = "/eqtl/variant_name/homo_sapiens/"+id["snp"]+"?statistic=p-value;stable_id="+id["ensg"]
    response = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if not response.ok:
        response.raise_for_status()
        sys.exit()

    pvalues = response.json()
    json_data.append({
        "snp" : id["snp"],
        "ensg" : id["ensg"],
        "data" : pvalues
    })
    print(json_data)

mode = os.environ.get('MODE')
if mode is None or mode == 'FILE':
    output_file = '/data/ensembl'+str(start)+"-"+str(end)+".json"
    with open(output_file, 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

else:
    response = requests.post("http://localhost:3000/transform", json = {"ensg":"a", "snp":"rs", "data":"MYDATA"})
    if not response.ok:
        response.raise_for_status()
        sys.exit()