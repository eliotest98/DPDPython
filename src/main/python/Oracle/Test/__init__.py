def get():
    # Create Tmp Folder
    if not os.path.isdir(TMP_FOLDER):
        print('Creating folder...')
        print('...', TMP_FOLDER)
        os.mkdir(TMP_FOLDER)