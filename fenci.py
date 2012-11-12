# -*- coding: UTF-8 -*-
import re
import sys

d = {}
def init(filename="SogouLabDic.dic"):
    f = open(filename, 'r')
    for line in f:
        word, freq = line.split('\t')[0:2]
        try:
            d[word.decode("gbk")] = int(freq)
        except:
            d[word] = int(freq)

def maxmatch(s):
    maxlen = 5
    l = len(s)
    p = 0
    result = {}
    while p < l:
        length = min(maxlen, l-p)
        wlen = 1
        for i in range(length, 0, -1):
            if d.has_key(s[p:p+i]):
                wlen = i
                break
        if wlen > 1:
            result.setdefault(s[p:p+wlen], 0)
            result[s[p:p+wlen]] += 1
        p += wlen

    return result

def maxmatch_back(s):
    maxlen = 5
    l = len(s)
    result = {}
    while l > 0:
        length = min(maxlen, l)
        wlen = 1
        for i in range(length, 0, -1):
            if d.has_key(s[l-i:l]):
                wlen = i
                break
        if wlen > 1:
            result.setdefault(s[l-wlen:l], 0)
            result[s[l-wlen:l]] += 1 
        l -= wlen

    return result
    
def one_word(s, start, rest=3):
    result = []
    maxlen = 5
    l = len(s)
    for former in start:
        p = former[len(former)-1]
        if p >= l: 
            result.append(former)
            break
        length = min(maxlen, l-p)
        num = 0
        for i in range(1, length+1):
            if d.has_key(s[p:p+i]):
                result.append(former + [p+i])
                num += 1
        if num == 0: result.append(former + [p+1])

    if rest > 1: return one_word(s, result, rest-1)
    else: return result
    
def three_word_chunk(s, start):
    result = one_word(s, [[start]], 3)
    longest = 0
    lset = []
    for i in range(len(result)):
        cur = result[i][len(result[i])-1] - result[i][0]
        if cur > longest:
            longest = cur
            lset = [i]
        elif cur == longest:
            lset.append(i)

    if len(lset) == 1:
        return result[lset[0]]
    else:
        # get the longest averge
        longavg = 0
        lavg = []
        for i in range(len(lset)):
            cur = longest / float(len(result[lset[i]])-1)
            if cur > longavg:
                longavg = cur
                lavg = [lset[i]]
            elif cur == longavg:
                lavg.append(lset[i])
        lset = lavg
        longest = longavg
        
    if len(lset) == 1:
        return result[lset[0]]
    else:
        # get the minmum dx
        mindk = sys.maxint
        dkset = []
        for i in range(len(lset)):
            cur = 0
            for j in range(1, len(result[lset[i]])):
                wordlen = result[lset[i]][j] - result[lset[i]][j-1]
                cur += pow((wordlen - longest), 2)
            
            if cur < mindk:
                mindk = cur
                dkset = [lset[i]]
            elif cur == mindk:
                dkset.append(lset[i])
        lset = dkset
        longest = mindk

    if len(lset) == 1:
        return result[lset[0]]
    else:
        # get the maxmum frequency
        maxFre = 0
        fset = []
        for i in range(len(lset)):
            cur = 0
            for j in range(1, len(result[i])):
                key = s[result[i][j-1]:result[i][j]]
                if d.has_key(key):
                    cur += d[key]
            if cur > maxFre:
                maxFre = cur
                fset = [lset[i]]
            elif cur == maxFre:
                fset.append(lset[i])
        lset = fset
        longest = maxFre

    if len(lset) == 1:
        return result[lset[0]]
    else:
#        print 'Really More than one...', lset
        return result[lset[0]]

# look ahead two more words
def mmseg(s):
    maxlen = 5
    l = len(s)
    p = 0

    result = {}
    while p < l:
        chunk = three_word_chunk(s, p)
        if(len(chunk) < 2): break

        if chunk[1] - chunk[0] > 1:
            result.setdefault(s[chunk[0]:chunk[1]], 0)
            result[s[chunk[0]:chunk[1]]] += 1
        p = chunk[1]
    return result

def solve(s, segment=maxmatch):
    s = s.decode("utf8")
    return segment(s)
