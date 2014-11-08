import sys
import pdb

def get_id(id_string):
	return id_string[6:-1]

def get_authors(author_string):
	return set( author_string[10:-1].split('; ') )

def compute_jaccard_index(s1, s2):
	a = len( s1.intersection(s2) )
	b = len( s1.union(s2) )
	jaccard = float(a)/float(b)		
	return jaccard

def get_current_paper_authors(current_paper_id):	
	fo = open('acl-metadata.txt')
	papers = fo.read().split('\n\n')[:-1] 	# to ignore the last blank element
	for paper in papers:
		info = paper.split('\n') 			# has an extra blank element at the end
		paper_id = get_id(info[0])
		if(paper_id == current_paper_id):
			current_paper_authors = get_authors(info[1])			
	print current_paper_authors
	return current_paper_authors

def compute_author_similarity(current_paper_id):
	current_paper_authors = get_current_paper_authors(current_paper_id)	
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

def compute_author_history(current_paper_id):
	current_paper_authors = get_current_paper_authors(current_paper_id)

if __name__=='__main__':
	current_paper_id = 'D10-1001'
	compute_author_similarity(current_paper_id)

	

