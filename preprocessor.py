import sys
import pdb

# supplementary function
def get_id(id_string):
	return id_string[6:-1]

# supplementary function
def get_authors(author_string):
	return set( author_string[10:-1].split('; ') )

# supplementary function
def compute_jaccard_index(s1, s2):
	a = len( s1.intersection(s2) )
	b = len( s1.union(s2) )
	jaccard = float(a)/float(b)		
	return jaccard

# supplementary function
def get_paper_authors(current_paper_id):	
	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1] 	# to ignore the last blank element
	for paper in papers:
		info = paper.split('\n') 			# has an extra blank element at the end
		paper_id = get_id(info[0])
		if(paper_id == current_paper_id):
			current_paper_authors = get_authors(info[1])			
	# print current_paper_authors
	return current_paper_authors

# supplementary function
def make_paper_author_dict():
	paper_authors_dict = {}
	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1] 	# to ignore the last blank element
	for paper in papers:
		info = paper.split('\n') 			# has an extra blank element at the end
		paper_id = get_id(info[0])
		paper_authors_dict[paper_id] = get_authors(info[1])
	return paper_authors_dict	

def compute_author_similarity(author_dict, current_paper_id):
	# current_paper_authors = get_paper_authors(current_paper_id)	
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
	# current_paper_authors = get_paper_authors(current_paper_id)
	current_paper_authors = author_dict[current_paper_id]
	author_history = {}

	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1]
	for paper in papers:
		common_authors_sum = 0
		info = paper.split('\n')
		paper_id = get_id(info[0])
		citers = papers_citing(paper_id)
#		for paper_2 in papers: 								
#			info_2 = paper_2.split('\n')
#			paper_id_2 = get_id(info_2[0])
#			if(paper_id_2 in citers and paper_id_2!=paper_id):
#				citer_authors = get_paper_authors(paper_id_2)
#				common_authors_sum += len( set(current_paper_authors).intersection(set(citer_authors)) )
		for citer in citers:
			if citer in author_dict.keys():
				citer_authors = author_dict[citer]
			else:
				citer_authors = []
			common_authors_sum += len( set(current_paper_authors).intersection(set(citer_authors)) )
		print "Number of common authors for "+paper_id+" = ",common_authors_sum		
		author_history[paper_id] = float(common_authors_sum)/len(current_paper_authors)
	print author_history

	fo = open('author_history_2.txt', 'w')
	for key,val in author_history.items():
		fo.write( key+'\t'+str(val)+'\n' )
	fo.close()

def compute_venue_relevancy(current_paper_id):


if __name__=='__main__':
	current_paper_id = 'D10-1001'
	author_dict = make_paper_author_dict()
	venue_dict = make_paper_
	compute_author_similarity(author_dict, current_paper_id)
	compute_author_history(author_dict, current_paper_id)