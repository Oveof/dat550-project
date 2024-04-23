import fastdup
import os
fd = fastdup.create(work_dir="./workdir",
                    input_dir="./data")
fd.run(ccthreshold=0.9, outlier_percentile=0.05)
broken_images = fd.invalid_instances()["filename"].to_list()
outliers = fd.outliers()["filename_outlier"].to_list()
print(broken_images)
print(outliers)
print(fd.connected_components())


def get_clusters(df, min_count=2):
    aggregate = {"filename": list, "max_distance": max, 'count': len}

    if 'label' in df.columns:
        aggregate['label'] = list

    df = df[df['count'] >= min_count]

    grouped_df = df.groupby('component_id').agg(aggregate)

    grouped_df = grouped_df.sort_values(by="count", ascending=False)

    return grouped_df


test, _ = fd.connected_components()
clusters_df = get_clusters(test)


singles = []
duplicates = []

for cluster_list in clusters_df.filename:
    single = cluster_list[0]
    singles.append(single)

    rest = cluster_list[1:]
    duplicates.append(rest)


for file in broken_images:
    file_name = file.split("/")[1]
    try:
        os.rename(f"./{file}", f"./data/invalid/{file_name}")
    except:
        pass
for file in outliers:
    file_name = file.split("/")[1]
    try:
        os.rename(f"./{file}", f"./data/outliers/{file_name}")
    except:
        pass
for files in duplicates:
    for file in files:
        file_name = file.split("/")[1]
        try:
            os.rename(f"./{file}", f"./data/duplicates/{file_name}")
        except:
            pass

fd.summary()
