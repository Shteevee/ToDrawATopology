[Net.ServicePointManager]::SecurityProtocol = "tls12, tls11, tls"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
Invoke-Expression "& `"..\..\..\python\bin\python`" .\get-pip.py"
Invoke-Expression "& `"..\..\..\python\Scripts\pip`" install numpy"
Invoke-Expression "& `"..\..\..\python\Scripts\pip`" install scikit-image"
Invoke-Expression "& `"..\..\..\python\Scripts\pip`" install svgwrite"
Remove-Item -path get-pip.py
pause