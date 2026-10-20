# -*- coding: utf-8 -*-
s = "\u00f0\u0178\u017d\u00ad"
b = s.encode('cp1252')
print("Encoded as cp1252:", b)
print("Decoded as utf-8:", b.decode('utf-8'))
