import sys
sys.path.append('../../')
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Links,Base,Urls,DomainsWhois,DomainsNetworkMetrics, get_db
import datetime
import igraph as ig
import numpy as np
import csv
import json


class ThreadNetworkMetrics:
    
    @staticmethod
    def retrieveDomains():

        #SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:309urje4@db:3306/debunker?"

        #engine = create_engine(
        #    SQLALCHEMY_DATABASE_URL,
        #    #connect_args={"check_same_thread": False}
        #)

        #SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        #Base.metadata.create_all(bind=engine)

        db=next(get_db())

        link_objects = db.query(Links).all()
        links = []
        for link_object in link_objects:
            if link_object.weight > 0:
                links.append([link_object.source, link_object.target,link_object.weight])

        G = ig.Graph.TupleList(edges=links,weights=True,directed=True)

        communities=G.community_walktrap().as_clustering()#edge_weights='weight')
        for community,index in zip(communities,range(0,len(communities))):
            for n in community:
                G.vs[n]['community']=index

        white_black={}
        white_black_list_file=open('Background/White and Black list.csv')
        for line in csv.DictReader(white_black_list_file,delimiter=',',quotechar='"'):
            if line['domain'] not in white_black:
                white_black[line['domain']]={ 'sources' : [],'list-type' : [] }
            white_black[line['domain']]['sources'].append(line['source'])
            white_black[line['domain']]['list-type'].append(line['list-type'])


        """hub_score = {G.vs["_nx_name"][i]: G.hub_score(weights='weight',vertices=i) for i in
             range(len(G.vs) - 1)}"""

        pagerank=G.pagerank( directed=True, weights='weight')
        pagerank = np.nan_to_num(pagerank)
        pagerank_norm = (pagerank - np.min(pagerank)) / (np.max(pagerank) - np.min(pagerank))
        pagerank_norm = np.nan_to_num(pagerank_norm)

        hub_score = G.hub_score(weights='weight')
        hub_score = np.nan_to_num(hub_score)
        hub_score_norm = (hub_score - np.min(hub_score)) / (np.max(hub_score) - np.min(hub_score))
        hub_score_norm = np.nan_to_num(hub_score_norm)

        authority_score = G.authority_score(weights='weight')
        authority_score = np.nan_to_num(authority_score)
        authority_score_norm = (authority_score - np.min(authority_score)) / (np.max(authority_score) - np.min(authority_score))
        authority_score_norm = np.nan_to_num(authority_score_norm)

        betweenness = G.betweenness(directed=True, weights=None)#, weights='weight') #non pesato perchè igraph considera il peso come distanza
        betweenness = np.nan_to_num(betweenness)
        betweenness_norm = (betweenness - np.min(betweenness)) / (np.max(betweenness) - np.min(betweenness))
        betweenness_norm = np.nan_to_num(betweenness_norm)

        closeness = G.closeness(weights='weight', mode='out')
        closeness = np.nan_to_num(closeness)
        closeness_norm = (closeness - np.min(closeness)) / (np.max(closeness) - np.min(closeness))
        closeness_norm = np.nan_to_num(closeness_norm)

        degrees_out=G.degree(G.vs, mode='out')

        degrees_in=G.degree(G.vs,mode='in')

        for node in G.vs:
            #domains_network_metrics=db.query(DomainsNetworkMetrics).filter(and_(DomainsNetworkMetrics.domain!='ilfattoquotidiano.it',DomainsNetworkMetrics.domain!='pianetablunews.it')).delete()
            domains_network_metrics=db.query(DomainsNetworkMetrics).filter(DomainsNetworkMetrics.domain==node['name']).first()
            if domains_network_metrics is not None:
                #domains_network_metrics.domain=node['name']
                #db.add(domains_network_metrics)
                domains_network_metrics.pagerank=float(pagerank_norm[node.index])
                domains_network_metrics.betweenness=float(betweenness_norm[node.index])
                domains_network_metrics.closeness=float(closeness_norm[node.index])
                domains_network_metrics.authority=float(authority_score_norm[node.index])
                domains_network_metrics.hub=float(hub_score_norm[node.index])
                domains_network_metrics.degree_out=float(degrees_out[node.index])
                domains_network_metrics.degree_in=float(degrees_in[node.index])

                weighted_neighbors = [[G.vs[neighbor]['name'],G.es[G.get_eid(node.index, neighbor,directed=True)]['weight']] for neighbor in G.neighbors(node['name'],mode='out')]
                weighted_neighbors.sort(key=lambda tup: tup[1], reverse=True)
                weighted_neighbors={'neighborhood_list':weighted_neighbors[0:14]+[['Other',int(np.sum([tup[1] for tup in weighted_neighbors[15:]]))]]}

                domains_network_metrics.neighborhood_list=json.dumps(weighted_neighbors)

                domains_network_metrics.white_list = {'sources': [],
                                                     'info': 'information about the sources from with we recover the whitelist'}
                domains_network_metrics.black_list = {'sources': [],
                                                     'info': 'information about the sources from with we recover the whitelist'}
                domains_network_metrics.is_blacklist = False
                if node['name'] in white_black:

                    for source,list_type in zip(white_black[node['name']]['sources'],
                                                white_black[node['name']]['list-type']):
                        if list_type == 'blacklist':
                            domains_network_metrics.is_blacklist=True
                            domains_network_metrics.black_list['sources'].append(source)
                        else:
                            domains_network_metrics.white_list['sources'].append(source)

                domains_network_metrics.black_list=json.dumps(domains_network_metrics.black_list)
                domains_network_metrics.white_list=json.dumps(domains_network_metrics.white_list)

                domains_network_metrics.white_community = 0
                domains_network_metrics.black_community = 0

                for n in communities[node['community']]:
                    if G.vs[n]['name'] in white_black:
                        if 'blacklist' in white_black[G.vs[n]['name']]['list-type']:
                            domains_network_metrics.black_community +=1
                        if 'whitelist' in white_black[G.vs[n]['name']]['list-type']:
                            domains_network_metrics.white_community +=1

                domains_network_metrics.white_community=domains_network_metrics.white_community/len(communities[node['community']])
                domains_network_metrics.black_community=domains_network_metrics.black_community/len(communities[node['community']])

                db.commit()
                #print(authority_score[i],hub_score[i])


if __name__ == "__main__":
    ThreadNetworkMetrics.retrieveDomains()