def progress(percent=0, width=30): #simple progress bar
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)


# import re
import csv
def check_training_file_integrity(filename):
    """A function to check that the only commas in our training datasets are the comma separators. This is rucial for the training of the neural network.

    Args:
        filename (str): name of the filenmae to analyze (with path)
    """
    # pattern = r",[012]$"

    with open(filename,"r") as f:
        for i,line in enumerate(f.readlines()):
            nb_of_commas = 0
            for char in line:
                if char == ",": nb_of_commas += 1

            if nb_of_commas > 1: #if there is more than one comma, then there is at least one too many !! 
                print(f"Line number: {i}, nb of commas: {nb_of_commas}")




        # fichier_reader = csv.reader(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # fichier_writer.writerow([siret, est_BIO, np.NaN])#, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN])



if __name__ == "__main__":

    validation = "/Users/leo/Desktop/Ecole/SciencesPo/S1/Socio_dig_pub_space/4_et_9-group_work/pythonneries/sociology_scrapping/tiktok_finetuning/data/validation.csv"
    train = "/Users/leo/Desktop/Ecole/SciencesPo/S1/Socio_dig_pub_space/4_et_9-group_work/pythonneries/sociology_scrapping/tiktok_finetuning/data/train.csv"

    check_training_file_integrity(validation)
    check_training_file_integrity(train)


