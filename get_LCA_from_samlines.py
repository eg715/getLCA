def get_LCA_from_sam(samlines,length_threshold,id_threshold,distance):
    from get_LCA_functions import taxidlist2LCA,find_parents,get_rank,find_rankofparents,name1, find_family,id_from_name
    nms=[]
    threshold=[]
    ids=[]
    lseqs=[]
##################sort lines by highest NM score###########
    for line in samlines:
        text=line.split()
        for i in text[11:len(text)]:
            if 'NM:' in i:
                nm=int(i.split(':')[2])
                nms.append(nm)

    samlines.sort(key=dict(zip(samlines, nms)).get)
    nms.sort()
    threshold=nms[0]+int(distance)
#########################append tax ids with NM score over 'threshold'#################
    for line,nm in zip(samlines,nms):
        text=line.split()
        taxid=text[2].split('|')[0]
        seq=text[9]
        l_seq=str(len(seq))

        if nm>threshold:
            break
        ids.append(taxid)
####################find LCA if more than 1 id has been accepted################
    try:
        lca=taxidlist2LCA(ids)
        family=find_family(lca)
        lca=':'.join(find_parents(lca)).replace(' ','_')
    except:
        lca='NOMATCH_TAXID_NOT_FOUND'
        family='FAMILY_NOT_FOUND'

    idp=nms[0]/float(l_seq)
    if float(l_seq)<float(length_threshold):
        lca='NOMATCH_length_below_'+str(length_threshold)+lca
    if (idp>(1-float(id_threshold))):#Similarity threshold set to 95%
        lca='NOMATCH_similarity_below_'+str(id_threshold)+lca

##################output line###############
    stats='tothits:'+str(len(samlines))+'_accepted-hits:'+str(len(ids))+'_Min-NM:'+str(nms[0])
    return('\t'.join([text[0],lca,get_rank(lca).replace(' ','_'),':'.join(ids),stats,l_seq,seq,family])+'\n')
