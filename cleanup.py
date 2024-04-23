import fastdup
import os
import csv
fd = fastdup.create(work_dir="./workdir",
                    input_dir="./data")
fd.run(ccthreshold=0.9, outlier_percentile=0.05)
broken_images = fd.invalid_instances()["filename"].to_list()
outliers = fd.outliers()["filename_outlier"].to_list()
# print(broken_images)
# print(outliers)
# print(fd.connected_components())


def get_clusters(f):
    aggregate = {"filename": list, "max_distance": max, 'count': len}

    if 'label' in f.columns:
        aggregate['label'] = list 

    df = f[f['count'] >= 2]

    grouped_df = df.groupby('component_id').agg(aggregate)

    grouped_df = grouped_df.sort_values(by="count", ascending=False)

    return grouped_df


test, _ = fd.connected_components()
clusters_df = get_clusters(test)
fd.vis.duplicates_gallery()

top_components = fastdup.find_top_components("./workdir")
fastdup.delete_components(top_components, how="one", dry_run=False)

print(len(top_components))
header = True
# for file in broken_images:
#     file_name = file.split("/")[1]
#     try:
#         os.rename(f"./{file}", f"./data/invalid/{file_name}")
#     except:
#         pass
# for file in outliers:
#     file_name = file.split("/")[1]
#     try:
#         os.rename(f"./{file}", f"./data/outliers/{file_name}")
#     except:
#         pass
# for files in duplicates:
#     for file in files:
#         file_name = file.split("/")[1]
#         try:
#             os.rename(f"./{file}", f"./data/duplicates/{file_name}")
#         except:
#             pass

with open("data/28k_apparel_data.csv") as f:
    with open("./modified_28k.csv", "a") as fa:
        csvFile = csv.reader(f)
        for line in csvFile:
            if header:
                header = False
                continue
            file = f"./data/{line[0]}.jpeg"
            if os.path.isfile(file):
                for x in range(len(line)):
                    table = str.maketrans("", "", "“”‘’\"\'")
                    line[x] = line[x].translate(table)
                    if "," in line[x]:
                        line[x] = f"\"{line[x]}\""

                fa.write(','.join(line) + "\n")


fd.summary()
