import sys
import pdb

# supplementary function
def get_id(id_string):
	return id_string[6:-1]

# supplementary function
def get_authors(author_string):
	return set( author_string[10:-1].split('; ') )

# supplementary function
def get_venue(venue_string):
	return venue_string[9:-1]	

# supplementary function
def compute_jaccard_index(s1, s2):
	a = len( s1.intersection(s2) )
	b = len( s1.union(s2) )
	jaccard = float(a)/float(b)		
	return jaccard

# supplementary function
def make_dicts():
	paper_authors_dict = {}
	paper_venue_dict = {}
	venue_venue_dict = {}
	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1] 	# to ignore the last blank element
	for paper in papers:
		info = paper.split('\n') 			# has an extra blank element at the end
		paper_id = get_id(info[0])
		paper_authors_dict[paper_id] = get_authors(info[1])
		venue = get_venue(info[3])
		paper_venue_dict[paper_id] = venue
		venue_venue_dict[venue] = {}
	print venue_venue_dict	
	return paper_authors_dict, paper_venue_dict, venue_venue_dict	

def compute_author_similarity(author_dict, current_paper_id):	
	current_paper_authors = author_dict[current_paper_id]
	jaccard_index = {}

	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1] 	# to ignore the last blank element
	for paper in papers:
		info = paper.split('\n')
		paper_id = get_id(info[0])
		paper_authors = get_authors(info[1])
		jaccard_index[paper_id] = compute_jaccard_index(current_paper_authors, paper_authors)
	fo = open('author_similarity.txt', 'w')
	for key,val in jaccard_index.items():
		fo.write( key+'\t'+str(val)+'\n' )	
	fo.close()

# supplementary function
def papers_citing(paper_id):
	citers = []
	f = open('acl.txt')
	cites = f.read().split('\n')[:-1]
	for cite in cites:
		papers = cite.split(' ==> ')
		if(papers[1] == paper_id):
			citers.append(papers[0])
	return citers			

def compute_author_history(author_dict, current_paper_id):
	current_paper_authors = author_dict[current_paper_id]
	author_history = {}

	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1]
	for paper in papers:
		common_authors_sum = 0
		info = paper.split('\n')
		paper_id = get_id(info[0])
		citers = papers_citing(paper_id)
		for citer in citers:
			if citer in author_dict.keys():
				citer_authors = author_dict[citer]
			else:
				citer_authors = []
			common_authors_sum += len( set(current_paper_authors).intersection(set(citer_authors)) )
		print "Number of common authors for "+paper_id+" = ",common_authors_sum		
		author_history[paper_id] = float(common_authors_sum)/len(current_paper_authors)
	print author_history

	fo = open('author_history.txt', 'w')
	for key,val in author_history.items():
		fo.write( key+'\t'+str(val)+'\n' )
	fo.close()

def compute_venue_relevancy(paper_venue_dict, venue_venue_dict, current_paper_id):
	current_venue = paper_venue_dict[current_paper_id]
	venue_relevancy = {}
	print "Current venue = ", current_venue

	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1]
	for paper in papers:
		info = paper.split('\n')
		paper_id = get_id(info[0])
		venue2 = paper_venue_dict[paper_id]
		citers = papers_citing(paper_id)
		for citer in citers:
			if citer in paper_venue_dict.keys():
				venue1 = paper_venue_dict[citer]
			else:
				venue1 = ""
			if venue1 == current_venue:
				if paper_id[:3] == 'P11':
					print "Venue same for ", citer
				if venue2 in venue_venue_dict[venue1].keys():	
					venue_venue_dict[venue1][venue2] += 1
				else:
					venue_venue_dict[venue1][venue2] = 1

	for paper in papers:
		info = paper.split('\n')
		paper_id = get_id(info[0])
		candidate_venue = paper_venue_dict[paper_id]
		if candidate_venue in venue_venue_dict[current_venue].keys():
			venue_relevancy[paper_id] = venue_venue_dict[current_venue][candidate_venue]
		else:
			venue_relevancy[paper_id] = 0

	fo = open('venue_relevancy.txt', 'w')
	for key,val in venue_relevancy.items():
		fo.write( key+'\t'+str(val)+'\n' )
	fo.close()					


if __name__=='__main__':
	current_paper_id = 'D10-1001'
	paper_author_dict, paper_venue_dict, venue_venue_dict = make_dicts()
#	compute_author_similarity(paper_author_dict, current_paper_id)
#	compute_author_history(paper_author_dict, current_paper_id)
	compute_venue_relevancy(paper_venue_dict, venue_venue_dict, current_paper_id)