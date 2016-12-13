import benfordspy.BenfordsPy as BP

test = BP.BenfordsPy()
data = test.analyzeexcel(filename='ABSi Bus Plan Rev N 090814.xlsx',
                  testtype="m",
                  wkshtincl={"BS"},
                  rowlblexcl={"Common stock"},
                  rowlblincldefault=True,
                  plottest=True,
                  printsignificance=True
                  )
