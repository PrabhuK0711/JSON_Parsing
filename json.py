import json
from datetime import datetime
from datetime import timedelta


def populate_data():
    # List of dicts for visits and hits to write to the output files in the end
    visits, hits = [], []
    # Parse the JSON data file to populate the lists visits and hits
    with open('ga_sessions_20160801.json') as file:
        # Loop to iterate over each line in the file which is one JSON record
        for line in file:
            visit_dict = {}
            data = json.loads(line)
            visit_dict['full_visitor_id'] = data['fullVisitorId']
            visit_dict['visit_id'] = data['visitId']
            visit_dict['visit_number'] = data['visitNumber']
            visit_dict['browser'] = data['device']['browser']
            visit_dict['country'] = data['geoNetwork']['country']
            visit_timestamp = int(data['visitStartTime'])
            visit_timestamp = datetime.utcfromtimestamp(visit_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            visit_dict['visit_start_time'] = visit_timestamp

            # Loop over the sub elements to get hits info
            for hit in data['hits']:
                hits_dict = {}
                # Below can be inserted to uniquely identify the hits records
                # hits_dict['unique_id'] = visit_dict['full_visitor_id'] + visit_dict['visit_id']
                hits_dict['hit_number'] = hit['hitNumber']
                hits_dict['hit_type'] = hit['type']
                millis = int(hit['time'])
                seconds = (millis / 1000) % 60
                s = int(seconds)
                minutes = (millis / (1000 * 60)) % 60
                m = int(minutes)
                hours = (millis / (1000 * 60 * 60)) % 24
                h = int(hours)
                # Add hit time to visits time
                hit_timestamp = datetime.strptime(visit_timestamp, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=s, minutes=m,
                                                                                                    hours=h)
                hits_dict['hit_timestamp'] = str(hit_timestamp)
                hits_dict['page_path'] = hit['page']['pagePath']
                hits_dict['page_title'] = hit['page']['pageTitle']
                hits_dict['hostname'] = hit['page']['hostname']

                # Append the dict to the list
                hits.append(hits_dict)
            visits.append(visit_dict)
    return visits, hits


def write_to_output_files(visits, hits):
    # Write the data to output files
    with open('visits.json', 'w') as file:
        for visit in visits:
            json.dump(visit, file)
            file.write("\n")

    with open('hits.json', 'w') as file:
        for hit in hits:
            json.dump(hit, file)
            file.write("\n")


def main():
    visits, hits = populate_data()
    write_to_output_files(visits, hits)

main()