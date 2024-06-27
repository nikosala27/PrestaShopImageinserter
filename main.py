from ImageInserter import ImageInserter


inserter = ImageInserter()
path = ''
images = inserter.get_product_images_from_directory(path)
shop = 'DE'

for key in images.keys():
    product_id = inserter.get_product_id_by_reference(key, shop)

    if product_id != '':
        inserter.insert_photo_on_last_pos(product_id, images[key][0], key, shop)

inserter.save_logs_to_file()
