#generate uu->Suu->chi chi-> Zt Zt (Z-> ll, Z-> ll)
sed -i '2 s/generate .*/generate p p \> suu, \(suu \> chi chi, \(chi \> z t, z \> l+ l-), \(chi \> z t, z \> l+ l-\)\)/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
sed -i '8 s/output .*/output \/data\/analysis\/iduminic\/diquark\-signal\/Zt\_ATLAS\_100k\-ll\-ll/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
nohup ./bin/mg5_aMC ZT_ATLAS_sgn_100k_136.dat > output_test_ll-ll.txt &

#generate uu->Suu->chi chi-> Zt Zt (Z-> ll, Z-> vl vl~)
sed -i '2 s/generate .*/generate p p \> suu, \(suu \> chi chi, \(chi \> z t, z \> l+ l-), \(chi \> z t, z \> vl vl\~\)\)/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
sed -i '8 s/output .*/output \/data\/analysis\/iduminic\/diquark\-signal\/Zt\_ATLAS\_100k\-ll\-vlvl/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
nohup ./bin/mg5_aMC ZT_ATLAS_sgn_100k_136.dat > output_test_ll-lvvl.txt &

#generate uu->Suu->chi chi-> Zt Zt (Z-> ll, Z-> jj)
sed -i '2 s/generate .*/generate p p \> suu, \(suu \> chi chi, \(chi \> z t, z \> l+ l-), \(chi \> z t, z \> j j\)\)/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
sed -i '8 s/output .*/output \/data\/analysis\/iduminic\/diquark\-signal\/Zt\_ATLAS\_100k\-ll\-jj/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
nohup ./bin/mg5_aMC ZT_ATLAS_sgn_100k_136.dat > output_test_ll-jj.txt &

#generate uu->Suu->chi chi-> Zt Zt (Z-> vlvl, Z-> jj)
sed -i '2 s/generate .*/generate p p \> suu, \(suu \> chi chi, \(chi \> z t, z \> vl vl\~), \(chi \> z t, z \> j j\)\)/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
sed -i '8 s/output .*/output \/data\/analysis\/iduminic\/diquark\-signal\/Zt\_ATLAS\_100k\-vlvl\-jj/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
nohup ./bin/mg5_aMC ZT_ATLAS_sgn_100k_136.dat > output_test_vlvl-jj.txt &

#generate uu->Suu->chi chi-> Zt Zt (Z-> vlvl, Z-> vlvl)
sed -i '2 s/generate .*/generate p p \> suu, \(suu \> chi chi, \(chi \> z t, z \> vl vl\~), \(chi \> z t, z \> vl vl\~\)\)/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
sed -i '8 s/output .*/output \/data\/analysis\/iduminic\/diquark\-signal\/Zt\_ATLAS\_100k\-ll\-vlvl/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
nohup ./bin/mg5_aMC ZT_ATLAS_sgn_100k_136.dat > output_test_ll-vlvl.txt &

#generate uu->Suu->chi chi-> Zt Zt (Z-> jj, Z-> jj)
sed -i '2 s/generate .*/generate p p \> suu, \(suu \> chi chi, \(chi \> z t, z \> j j), \(chi \> z t, z \> j j\)\)/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
sed -i '8 s/output .*/output \/data\/analysis\/iduminic\/diquark\-signal\/Zt\_ATLAS\_100k\-jj\-jj/1' diquark-signal-Zt/ZT_ATLAS_sgn_100k_136.dat
nohup ./bin/mg5_aMC ZT_ATLAS_sgn_100k_136.dat > output_test_jj-jj.txt &