#!/usr/bin/env python
import numpy as np
import datetime
import time

from stream_tweets_to_slack import real_time_tweets


if __name__ == "__main__":

    query_file_path = "./sample_queries.txt"
    
    init_first_time = True 
    while True:

        if init_first_time:
            init_first_time = 0
            with open(query_file_path, "r") as f:
                query_content = f.readlines()
            query_list = [x.strip() for x in query_content]
        
            list_last_ids = np.array([])
            print("Initializing all queries for the first time")
            for query in query_list:
                last_id = real_time_tweets(query, first_time=True)
                list_last_ids = np.append(list_last_ids, last_id)

        ind_flag = 0
        for query in query_list:
            last_id = real_time_tweets(query, last_tweet_id=list_last_ids[ind_flag])
            if last_id != list_last_ids[ind_flag]:
                list_last_ids[ind_flag] = last_id
            ind_flag += 1

        print("Last refreshed for new tweets at", datetime.datetime.now())
        time.sleep(20)