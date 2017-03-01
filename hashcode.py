import sys
input_lines = sys.stdin.readlines()
details = input_lines[0].split()
videos = input_lines[1].split()
cache_limit = details[4]
caches = [int(details[4])]* int(details[3])
videos_in_cache = {}
cache_connected_to_endpoints = {}
videos_in_a_cache = []
# Cache stores for output
for i in range(int(details[3])):
	videos_in_cache[i] = []

# Class for endpoints
class Endpoint(object):

	def __init__(self,endpoint_id,datacenter_latency,cache_latencies):
		if cache_latencies == None:
			self.cache_latencies = {}
		self.endpoint_id = endpoint_id
		self.datacenter_latency = datacenter_latency


# Class for scoring the request descriptors
class Score(object):
	def __init__(self,video_id,endpoint_id,no_of_requests,cache_latency):
		self.video_id = video_id
		self.endpoint_id = endpoint_id
		self.no_of_requests = no_of_requests
		self.score = (int(self.no_of_requests)/int(videos[int(self.video_id)]))

# Build endpoints
endpoints = []
i = 0
k = 0
endpoint_line = input_lines[2+k].split()
k = 1
while i < int(details[1]):
	current_endpoint = Endpoint(i,endpoint_line[0],None)
	j = 0
	while j < int(endpoint_line[1]):
		current_line = input_lines[2+k+i].split()
		current_endpoint.cache_latencies[str(current_line[0])] = str(current_line[1])
		if str(current_line[0]) in cache_connected_to_endpoints:
			cache_connected_to_endpoints[str(current_line[0])] += 1
		else:
			cache_connected_to_endpoints[str(current_line[0])] = 1
		j += 1
		k += 1
	endpoints.append(current_endpoint)
	endpoint_line = input_lines[2+k+i].split()
	i += 1


# Build scores
scores = []
i = 0
while i < int(details[2]):
	current_line = input_lines[-1-i].split()
	for cache in endpoints[int(current_line[1])].cache_latencies:
		new_score = Score(current_line[0],current_line[1],current_line[2],endpoints[int(current_line[1])].cache_latencies[cache])
		scores.append([new_score.score*int(endpoints[int(current_line[1])].cache_latencies[cache]),new_score.endpoint_id,current_line[0],cache,videos[int(current_line[0])]])
	i += 1

# Sorting the scores
scores = sorted(scores)

# Allocate cache space
allocations = 1
while allocations > 0:
	allocations = 0
	for s in range(len(scores)):
			if(caches[int(scores[s][3])] > int(videos[int(scores[s][2])])) and scores[s][2] not in videos_in_cache[int(scores[s][3])] and scores[s][2] not in videos_in_a_cache and (int(scores[s][3]))/int(endpoints[int(scores[s][1])].datacenter_latency) <=(int(scores[s][4])/int(cache_limit))/4:
				caches[int(scores[s][3])] -= int(videos[int(scores[s][2])])
				videos_in_cache[int(scores[s][3])].append(scores[s][2])
				videos_in_a_cache.append(scores[s][2])
				allocations += 1

for s in range(len(scores)):
	if(caches[int(scores[s][3])] > int(videos[int(scores[s][2])])) and scores[s][2] not in videos_in_cache[int(scores[s][3])] and (int(scores[s][3]))/int(endpoints[int(scores[s][1])].datacenter_latency) <= (int(scores[s][4])/int(cache_limit)):
		caches[int(scores[s][3])] -= int(videos[int(scores[s][2])])
		videos_in_cache[int(scores[s][3])].append(scores[s][2])
		videos_in_a_cache.append(scores[s][2])


# Output the answer
print(len(videos_in_cache.keys()))
for key in sorted(videos_in_cache.keys()):
	print(str(key) + " " + " ".join(videos_in_cache[key]))
