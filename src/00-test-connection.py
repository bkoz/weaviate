import weaviate_utils
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    client = weaviate_utils.weaviate_connection()

    logging.info('')
    if client.is_ready():
        logging.info('get_nodes_status(): %s', client.cluster.get_nodes_status())
        logging.info('')