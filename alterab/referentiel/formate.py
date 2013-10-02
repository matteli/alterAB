from oosheet import OOSheet as S
import json
import string

def formate( ):
    r=[]
    r = tab2json('Config_referentiel', r)
    r = tab2json('Savoir', r)
    r = tab2json('Groupe_savoir', r)
    r = tab2json('Competence', r)
    r = tab2json('Groupe_competence', r)
    r = tab2json('Tache', r)
    r = tab2json('Groupe_tache', r)
    r = tabm2m2json('Competence_dans_tache', r)
    
    writeFile(r, '/home/matthieu/refjson.txt')
    return None
    
def tab2json(feuille, r):
    j=2
    while S(feuille + '.a' + unicode(j)).string != "":
        num = S(feuille + '.a' + unicode(j)).string
        i=1
        field={}
        while S(feuille + '.' + string.lowercase[i] + '1').string != "":
            field[S(feuille + '.' + string.lowercase[i] + '1').string]=S(feuille + '.' + string.lowercase[i] + unicode(j)).string
            i=i+1
        j=j+1
        entry = {
            u"model":u"suivi." + feuille,
            u"pk":num,
            u"fields":field,
        }
        r.append(entry)

    return r

def tabm2m2json(feuille, r):
    tab1=S(feuille + '.a2').string
    tab2=S(feuille + '.b1').string
    rel=S(feuille + '.b2').string
    pk=0
    i=3
    while S(feuille + '.a' + unicode(i)).string != "" and S(feuille + '.a' + unicode(i)).string != "0":
        j=2
        while S(feuille + '.' + string.lowercase[j] + '1').string != "" and S(feuille + '.' + string.lowercase[j] + '1').string != "0" :
            try:
                num = int(float(S(feuille + '.' + string.lowercase[j] + unicode(i)).string))
            except:
                num = 0
            if num>0:
                pk=pk+1
                entry = {
                    u"model":u"suivi." + feuille,
                    u"pk":pk,
                    u"fields":{
                        rel:num,
                        tab1:i-2,
                        tab2:j-1,
                    },
                }
                r.append(entry)
            j=j+1
        i=i+1
    return r

def writeFile(source, name):
    rjson=json.JSONEncoder().encode(source)
    f = open(name, 'w')
    f.write(rjson)
    f.closed
    return None
