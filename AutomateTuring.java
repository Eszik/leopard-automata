// javac -target 1.5 -source 1.5 -encoding UTF-8 Cours4.java

// setenv CLASSPATH .:/Users/ielm/Downloads/simulab/Simulab.jar

// appletviewer cours2_test_v3.html &

// ant compilation
// ant execution
import simu.*;
import java.util.*;
import java.awt.*;
import maillage.*;
import tflib.*;
import transforms.fft.*;
import java.io.*;
import java.lang.*;

/**Ceci est la classe <b>AutomateTuring</b> qui constitue un premier essai de
 * réalisation d'une applet Java présentant
 * l'évolution d'une structure selon le modèle de Turing.
 */

public class AutomateTuring extends SimuApplet {


    // Input
    double rcinit;
    double r1;
    double r2;
    double j1;
    double j2;
    double offset;
    double nbrevoronoy;
    int nstep;
    String grille;
    String geometrie;
    String ajuster;
    String machine;
    String synchro;
    String texteapplet;
    String powerlog;
    String couleur1;
    String couleur2;
    
    boolean powerlog_bool;
    
    double[] sizeileyk;
    double[] fftileyk;
    
    // Output
    //double[][] taches;
    double[][] fft;
    double lc;
    int somme;
    int nbcell;

    /** Grandeurs courantes
     */
    int tpsactuel;
    int dimx;
    int dimy;
    int gamma;
    Image imgtaches;
    Graphics graphtaches;

    /**Essai de grille
     */
    int nlignes;
    int ncolonnes;
    Grille taches;

    int[] liste;    
    boolean[] dejavu;

    /**Constructeur de la classe, avec définition des paramètres de simulation
     *et des options d'affichage.
     */
    public AutomateTuring() {
        appletDoc("AutomateTuring_website.xml");
    }


    /** Méthode initialisant l'affichage de l'applet
     * 
     * @param ListeValeurs
     * Liste de valeurs en entrée (voir SimuLab)
     */
    public void initCalculLive(ListeValeurs in) throws SimuException {
        
        machine = in.lireString("machine");
        r1 = in.lireDouble("r1");
        r2 = in.lireDouble("r2");
        j1 = in.lireDouble("diff1");
        j2 = in.lireDouble("diff2");
        offset = in.lireDouble("offset");  
        nstep = in.lireEntier("nstep");
        grille = in.lireString("grille");
        geometrie = in.lireString("geometrie");
        synchro=in.lireString("synchro");
        powerlog=in.lireString("powerlog");
        couleur1=in.lireString("couleur1");
        couleur2=in.lireString("couleur2");
        nbrevoronoy=in.lireDouble("pointsvoronoy");
        System.out.println("Fin de la lecture dans InitCalculLive");
        //ajuster = in.lireString("ajuster");
        
        if (powerlog.equals("logarithmic")){
            powerlog_bool=true;
        }
        else {
            powerlog_bool=false;
        }
       
        tpsactuel=0;
        //dimx=200;
        //dimy=200;
        //taches = new double[dimx][dimy];


        /** Ces fonctions permettent de recadrer  à chaque itération pour lc            
        * et somme, ou pour différents dimx et dimy pour taches et fft les 
        *affichages en solo mais ne fonctionnent pas en mode multiplot (pour qu'ils
        *fonctionnent, il faut spécifier les memes dimensions dans le .xml,
        * aucun intérêt). Il faut donc faire une boucle if sur le fait que
        *l'utilisateur choisisse un affichage en solo (auquel cas on redimensionne)
        *ou un affichage 4 panneaux (auquel cas on laisse multiplot dimensionner
        * comme il le souhaite)
        */
        if(machine.equals("Modeste")){
            if(geometrie.equals("corps")){
                dimx=128;
                dimy=128;
            }
            else if (geometrie.equals("queue")){
                dimx=128;
                dimy=10;
            }
        }
        if(machine.equals("Puissante")){
            if(geometrie.equals("corps")){
                dimx=512;
                dimy=512;
            }
            else if (geometrie.equals("queue")){
                dimx=512;
                dimy=40;
            }
        }
        if(machine.equals("Moyenne")){
            if(geometrie.equals("corps")){
                dimx=256;
                dimy=256;
            }
            else if (geometrie.equals("queue")){
                dimx=256;
                dimy=20;
            }
        }

        imgtaches=createImage(dimx,dimy);
        graphtaches=imgtaches.getGraphics();
        Affichage affimage = getAffichage("tachimage");
        // Ici "tachimage" est le label de l'affichage considéré dans Jaxe.
        // Il s'agit ici de l'affichage des taches seules.
        affimage.imgdimx = dimx;
        affimage.imgdimy = dimy; 
        //Affichage affimage2 = getAffichage("fftimage");
        // Ici il s'agit de l'affichage de la fft seule.
        //affimage2.imgdimx = dimx;
        //affimage2.imgdimy = dimy; 

        Affichage qafftot = getAffichage("4panneauximage");
        // Ici on récupère l'affichage multiple des quatre panneaux.
        Affichage qafftaches;
        Affichage qafffft;
        qafftaches= qafftot.sousAff[0];
        qafffft= qafftot.sousAff[2];
        // Récupération des taches dans l'affichage multiple.
        qafftaches.imgdimx = dimx;
        qafftaches.imgdimy = dimy; 
        // Récupération de la fft dans l'affichage multiple.
        qafffft.imgdimx = dimx;
        qafffft.imgdimy = dimy; 

        Affichage ffqafftot = getAffichage("4panneauxdefftimage");
        // Ici on récupère l'affichage multiple des quatre panneaux.
        Affichage ffqafftaches;
        Affichage ffqafffft;
        ffqafftaches= ffqafftot.sousAff[0];
        ffqafffft= ffqafftot.sousAff[2];
        // Récupération des taches dans l'affichage multiple.
        ffqafftaches.imgdimx = dimx;
        ffqafftaches.imgdimy = dimy; 
        // Récupération de la fft dans l'affichage multiple.
        ffqafffft.imgdimx = dimx;
        ffqafffft.imgdimy = dimy; 

        /** Création de la grille
         * Cette grille s'appelle "taches" et sera actualisée au gré de la vie
         * et de la mort des cellules.
         * Ses dimensions sont dimx*dimy=nbcell, le nombre de cellules, dans le cas de la grille carrée.
         */
       
        /** Grille carrée -----------------------------------------------------------
         */
        
        if (grille.equals("Simple")){
            taches= new GrilleCarree(dimx,dimy);
       
            nbcell=dimx*dimy;

            // Ici on cree les vecteurs de voisins dans les cellules, rayon rr2 le plus grand
            System.out.println("debut de l'init des voisins");
            for (int ii=0; ii<nbcell;ii++) { 
                taches.rechercheVoisins(ii,(int)r2);
                //System.out.println("voisin i="+ii+"sur "+nbcell); // <--- compteur eventuel
            }
            System.out.println("fin de l'init des voisins");

            /** Création du tableau fft.
             */
            fft = new double[dimx][dimy];

            /** tableau dejavu pour l'evolution semi-asynchrone
             */

            dejavu = new boolean[dimx*dimy];
            /*liste = new int[dimx*dimy];
             for (int i=0; i<dimx*dimy ; i++) {
            liste[i]=i;
             }*/
           
            // ---------------------------------------------------------------------------------------------------
            
             // Fixe toute la grille à 0
            /*for (int i=0; i<dimx*dimy ; i++) {
                if (((taches.getCellule(i)).statut()==true)) {
                    (taches.getCellule(i)).changementStatut();
                }
            }
            
            // Fait 10 trous de rayon r2 dans la grille
            for (int k=0; k<10 ; k++) {
                int indicerand=(int)(dimx*dimy*Math.random());
                (taches.getCellule(indicerand)).changementStatut();
                Cellule cellule_test=taches.getCellule(indicerand);
                Vector<Cellule> v = cellule_test.getVoisins(); 
                for (int i=0; i<v.size() ; i++) {
                    if ((v.get(i)).statut()==false) {
                        (v.get(i)).changementStatut();     
                    }
                }
            }   */
            
           // ---------------------------------------------------------------------------------------------------
            
            
        }

        /** Grille hexagonale ------------------------------------------------------------
         */
        if (grille.equals("Hexagonale")){

            System.out.println("Hexa commence");
            taches= new GrilleHexa(dimx,dimy);
            nbcell=dimx*dimy;
            // Ici on cree les vecteurs de voisins dans les cellules, rayon rr2 le plus grand
            System.out.println("debut de l'init des voisins"+"nbcell"+nbcell);
            for (int ii=0; ii<nbcell;ii++) {
                taches.rechercheVoisins(ii,(int)r2);
                //System.out.println("voisin i="+ii+"sur "+nbcell); // <--- compteur eventuel
            }
            System.out.println("fin de l'init des voisins");

            /** Création du tableau fft.
             */
            fft = new double[dimx][dimy];

            /** tableau dejavu pour l'evolution semi-asynchrone
             */
            dejavu = new boolean[dimx*dimy];

            System.out.println("Fin de InitCalculLive");
        }
        
        /** Grille VORONOY ------------------------------------------------------------
         */
        if (grille.equals("Voronoy")){
            
            System.out.println("Voro commence");
            taches= new GrilleVoronoi(dimx,(int)(nbrevoronoy*((double)(dimx*dimx))));
            nbcell=(int)(nbrevoronoy*((double)(dimx*dimx)));
            // Ici on cree les vecteurs de voisins dans les cellules, rayon rr2 le plus grand
            System.out.println("debut de l'init des voisins"+"nbcell"+nbcell);
            for (int ii=0; ii<nbcell;ii++) {
                taches.rechercheVoisins(ii,(int)r2); 
                //System.out.println("voisin i="+ii+"sur "+nbcell); // <--- compteur eventuel
            }
            System.out.println("fin de l'init des voisins");
            
            /** Création du tableau fft.
             */
            fft = new double[dimx][dimy];
            
            /** tableau dejavu pour l'evolution semi-asynchrone
             */
            dejavu = new boolean[dimx*dimy];
            
            System.out.println("Fin de InitCalculLive");
        }
        
        // ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
        sizeileyk = new double[dimx/2];
        //System.out.println(dimx/2);
        /*for (int i=0; i<dimx/2; i++){
         sizeileyk[i]=(double)i;
         //System.out.println(sizeileyk[i]);
         }*/
        fftileyk = new double[dimx/2];
        // ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

            //System.out.println("Taille maximum de la gommette : "+Math.min(dimx,dimy)/2);
        
    }

    

    /** Fait le calcul en temps réel 
     * 
     * @return ListeValeurs
     * Affiche l'image suivante dans la fenêtre.
     * @throws SimuException si souci d'affichage
     */

    public ListeValeurs calculLive() throws SimuException {
        ListeValeurs out = new ListeValeurs();
        
        double echelle_tache ;
        echelle_tache=0.;
        
        // Cas d'une grille carrée---------------------------------------------------
        if (grille.equals("Simple")){

            if (synchro.equals("asynchrone")) {
                double indiceranddouble;
                int indicerand;
                for(int k=0; k<nstep;k++){
                    indiceranddouble=dimx*dimy*Math.random();
                    indicerand=(int)indiceranddouble;
                    evolution_grille_asynchrone(indicerand,taches,r1,r2,j1,j2,offset); //pas besoin de sortir la grille car c'est un objet, pas le cas avec types simples
                    //objet de la classe double
                }
            }
            else if (synchro.equals("synchrone")) {
                Grille tachesold= taches;
                for(int k=0; k<(int)(dimx*dimy);k++){
                    evolution_grille_synchrone(k,tachesold,taches,r1,r2,j1,j2,offset); 
                }
            }
            else if (synchro.equals("semi-asynchrone")) {
                int indicerand;

                Arrays.fill(dejavu, Boolean.FALSE);

                for(int k=0; k<dimx*dimy;k++){
                    indicerand=(int)(((double)dimx*dimy)*Math.random());
                    if (dejavu[indicerand]==true) {
                        //System.out.println(k+" "+indicerand);
                        while (dejavu[indicerand]==true) {
                            //	System.out.println(k+" "+indicerand);
                            //	indicerand=(indicerand+1)%(dimx*dimy); // risque de biais
                            indicerand=(int)(((double)dimx*dimy)*Math.random());
                        }
                    }
                    dejavu[indicerand]=true;

                    //System.out.println(k+" "+indicerand);
                    //System.out.println(dejavu[3]);

                    evolution_grille_asynchrone(indicerand,taches,r1,r2,j1,j2,offset);
      
                }
                
                // Permutation 2 à 2 : ne change pas significativement la vitesse d'exécution...
                /* for(int p=0; p<(int)(((double)(dimx*dimy)));p++){
                 int indicerand1=(int)(((double)dimx*dimy)*Math.random());
                 int indicerand2=(int)(((double)dimx*dimy)*Math.random());
                 //System.out.println(indicerand1+" "+indicerand2);
                 int temp=liste[indicerand1];
                 liste[indicerand1]=liste[indicerand2];
                 liste[indicerand2]=temp;
                 }
                 for(int k=0; k<dimx*dimy;k++){
                 if (k==1) {      
                 System.out.println(k);
                 }
                 k=liste[k];
                 evolution_grille_asynchrone(k,taches,r1,r2,j1,j2,offset);
                 }*/
        
            }

            somme=0;
     
            for(int iii=0;iii<(nbcell);iii++){
                if(((taches.getCellule(iii)).statut())==true){
                    somme=somme+1;
                }
                else{
                    somme=somme-1;
                }
            }
       
            /**Après, on calculera la FFT de cette nouvelle configuration
             * Puis on extraiera les valeurs de lc et de somme
             */
            double liste_moy[] ;
            double liste_derive[] ;  
            double taches_conv[][] ;
            //liste_moy = correlation((GrilleCarree)taches) ; // <====== Mdification pour prendre en entrée n'importe quelle grille ! ok
            taches_conv=taches.conversion(dimx,dimy,1) ;
            liste_moy = correlation(taches_conv) ;
            
            liste_derive = derivee(liste_moy) ;
            // System.out.println("fin du calcul de liste_moy de taille "+liste_moy.length);
            for (int i=0; i<liste_moy.length; i++) {
                out.ajouter("lc",(double)liste_moy[i]);
                out.ajouter("lcderiv",(double)liste_derive[i]);
                out.ajouter("lcx",(double)i);          
            }
            
            echelle_tache = taille_caracteristique (liste_moy, liste_derive);
            //System.out.println("Taille caracteristique des taches : "+echelle_tache+" pixels.") ;
            //out.ajouterString("texteapplet", "Taille caractéristique calculée: "+(float)echelle_tache+" pixels.");
            
            // Palette de couleur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            //System.out.println("Couleurs now : "+couleur1+" "+couleur2);
            if (couleur1.equals("noir")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.black);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.black);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.black);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.black);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.black);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.black);
                }
            }
            else if (couleur1.equals("blanc")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.white);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.white);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.white);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.white);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.white);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.white);
                }
            }
            else if (couleur1.equals("orange")) {
                if (couleur2.equals("white")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.orange);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.orange);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.orange);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.orange);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.orange);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.orange);
                }
            } 
            if (couleur1.equals("jaune")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.yellow);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.yellow);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.yellow);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.yellow);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.yellow);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.yellow);
                }
            }
            if (couleur1.equals("rouge")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.red.darker());
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.red.darker());
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.red.darker());
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.red.darker());
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.red.darker());
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.red.darker());
                }
            }    
            if (couleur1.equals("vert")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.green.darker());
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.green.darker());
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.green.darker());
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.green.darker());
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.green.darker());
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.green.darker());
                }
            }    
            if (couleur1.equals("bleu")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.blue);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.blue);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.blue);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.blue);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.blue);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.blue);
                }
            }    
            // Palette de couleur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            
            out.ajouter("taches",imgtaches);
            //out.ajouterDouble("lc",lc);
            //out.ajouter("fft",fft);
            out.ajouterDouble("somme",(double)(somme)/((double)dimx*(double)dimy));
            out.ajouterDouble("tpsactuel",(double)(tpsactuel));
            out.ajouterDouble("lcnow",echelle_tache);
           
   
            //out.ajouterString("tpsactuel", "iteration en cours:"+tpsactuel);        
            tpsactuel++;

  
       
        }

        //Cas d'une grille hexagonale -----------------------------------------------------
        if(grille.equals("Hexagonale")){
            
            if (synchro.equals("asynchrone")) {
                double indiceranddouble;
                int indicerand;
                for(int k=0; k<nstep;k++){
                    indiceranddouble=dimx*dimy*Math.random();
                    indicerand=(int)indiceranddouble;
                    evolution_grille_asynchrone(indicerand,taches,r1,r2,j1,j2,offset); //pas besoin de sortir la grille car c'est un objet, pas le cas avec types simples
                    //objet de la classe double
                }
            }
        
            else if (synchro.equals("synchrone")) {
                Grille tachesold=taches;
                for(int k=0; k<(int)(dimx*dimy);k++){
                    evolution_grille_synchrone(k,tachesold,taches,r1,r2,j1,j2,offset); 
                }
            }
            else if (synchro.equals("semi-asynchrone")) {
                 
                int indicerand;
                Arrays.fill(dejavu, Boolean.FALSE);
                for(int k=0; k<dimx*dimy;k++){
                    indicerand=(int)(((double)dimx*dimy)*Math.random());
                    if (dejavu[indicerand]==true) {
                        //System.out.println(k+" "+indicerand);
                        while (dejavu[indicerand]==true) {
                            //	System.out.println(k+" "+indicerand);
                            //	indicerand=(indicerand+1)%(dimx*dimy); // risque de biais
                            indicerand=(int)(((double)dimx*dimy)*Math.random());
                        }
                    }
                    dejavu[indicerand]=true;

                    //System.out.println(k+" "+indicerand);
                    //System.out.println(dejavu[3]);

                    evolution_grille_asynchrone(indicerand,taches,r1,r2,j1,j2,offset);

                }

            }
    
            somme=0;
     
            for(int iii=0;iii<(nbcell);iii++){
                if(((taches.getCellule(iii)).statut())==true){
                    somme=somme+1;
                }
                else{
                    somme=somme-1;
                }
            }
       
            /**Après, on calculera la FFT de cette nouvelle configuration
             * Puis on extraiera les valeurs de lc et de somme
             */
            double liste_moy[] ;
            double liste_derive[] ;
            double taches_conv[][] ;

            taches.conversionGraphics(graphtaches,1,Color.black,Color.orange);
            out.ajouter("taches",imgtaches);
        
            //out.ajouterDouble("lc",lc);
            //out.ajouter("fft",fft);
    
            out.ajouterDouble("somme",(double)(somme)/((double)dimx*(double)dimy));
            out.ajouterDouble("tpsactuel",(double)(tpsactuel)); 

            taches_conv=taches.conversion(dimx,dimy,1) ;

            liste_moy = correlation(taches_conv) ; 
            liste_derive = derivee(liste_moy) ;

            // A adapter à la grille hexagonale
            for (int i=0; i<liste_moy.length; i++) {
                out.ajouter("lc",(double)liste_moy[i]);
                out.ajouter("lcderiv",(double)liste_derive[i]);
                out.ajouter("lcx",(double)i);          
            }

            echelle_tache = taille_caracteristique (liste_moy, liste_derive);
            //System.out.println("Taille caracteristique des taches : "+echelle_tache+" pixels.") ;
            
            // Palette de couleur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            //System.out.println("Couleurs now : "+couleur1+" "+couleur2);
            if (couleur1.equals("noir")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.black);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.black);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.black);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.black);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.black);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.black);
                }
            }
            else if (couleur1.equals("blanc")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.white);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.white);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.white);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.white);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.white);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.white);
                }
            }
            else if (couleur1.equals("orange")) {
                if (couleur2.equals("white")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.orange);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.orange);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.orange);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.orange);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.orange);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.orange);
                }
            } 
            if (couleur1.equals("jaune")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.yellow);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.yellow);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.yellow);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.yellow);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.yellow);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.yellow);
                }
            }
            if (couleur1.equals("rouge")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.red.darker());
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.red.darker());
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.red.darker());
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.red.darker());
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.red.darker());
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.red.darker());
                }
            }    
            if (couleur1.equals("vert")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.green.darker());
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.green.darker());
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.green.darker());
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.green.darker());
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.green.darker());
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.green.darker());
                }
            }    
            if (couleur1.equals("bleu")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.blue);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.blue);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.blue);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.blue);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.blue);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.blue);
                }
            }    
            // Palette de couleur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            
            //out.ajouterString("texteapplet", "Taille caractéristique calculée: "+(float)echelle_tache+" pixels.");       
            out.ajouterDouble("lcnow",echelle_tache);

            
            tpsactuel++;
            
            
       
        }
        
        
        //Cas d'une grille VORONOY -----------------------------------------------------
        if(grille.equals("Voronoy")){
            
            if (synchro.equals("asynchrone")) {
                double indiceranddouble;
                int indicerand;
                for(int k=0; k<nstep;k++){
                    indiceranddouble=dimx*dimy*Math.random();
                    indicerand=(int)indiceranddouble;
                    evolution_grille_asynchrone(indicerand,taches,r1,r2,j1,j2,offset); //pas besoin de sortir la grille car c'est un objet, pas le cas avec types simples
                    //objet de la classe double
                }
            }
            
            else if (synchro.equals("synchrone")) {
                Grille tachesold=taches;
                for(int k=0; k<(int)(dimx*dimy);k++){
                    evolution_grille_synchrone(k,tachesold,taches,r1,r2,j1,j2,offset); 
                }
            }
            else if (synchro.equals("semi-asynchrone")) {
                
                int indicerand;
                Arrays.fill(dejavu, Boolean.FALSE);
                for(int k=0; k<(int)(nbrevoronoy*((double)(dimx*dimx)));k++){
                    indicerand=(int)((nbrevoronoy*((double)(dimx*dimx)))*Math.random());
                    if (dejavu[indicerand]==true) {
                        //System.out.println(k+" "+indicerand);
                        while (dejavu[indicerand]==true) {
                            //	System.out.println(k+" "+indicerand);
                            //	indicerand=(indicerand+1)%(dimx*dimy); // risque de biais
                            indicerand=(int)((nbrevoronoy*((double)(dimx*dimx)))*Math.random());
                        }
                    }
                    dejavu[indicerand]=true;
                    
                    //System.out.println(k+" "+indicerand);
                    //System.out.println(dejavu[3]);
                    
                    evolution_grille_asynchrone(indicerand,taches,r1,r2,j1,j2,offset);
                    
                }
                
            }
            
            somme=0;
            
            for(int iii=0;iii<(nbcell);iii++){
                if(((taches.getCellule(iii)).statut())==true){
                    somme=somme+1;
                }
                else{
                    somme=somme-1;
                }
            }
            
            /**Après, on calculera la FFT de cette nouvelle configuration
             * Puis on extraiera les valeurs de lc et de somme
             */
            double liste_moy[] ;
            double liste_derive[] ;
            double taches_conv[][] ;
            
            taches.conversionGraphics(graphtaches,1,Color.black,Color.orange);
            out.ajouter("taches",imgtaches);
            
            //out.ajouterDouble("lc",lc);
            //out.ajouter("fft",fft);
            
            out.ajouterDouble("somme",(double)(somme)/((double)dimx*(double)dimy));
            out.ajouterDouble("tpsactuel",(double)(tpsactuel)); 
            
            taches_conv=taches.conversion(dimx,dimy,1) ;
            
            liste_moy = correlation(taches_conv) ; 
            liste_derive = derivee(liste_moy) ;
            
            for (int i=0; i<liste_moy.length; i++) {
                out.ajouter("lc",(double)liste_moy[i]);
                out.ajouter("lcderiv",(double)liste_derive[i]);
                out.ajouter("lcx",(double)i);          
            }
            
            echelle_tache = taille_caracteristique (liste_moy, liste_derive);
            //System.out.println("Taille caracteristique des taches : "+echelle_tache+" pixels.") ;
            
            // Palette de couleur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            //System.out.println("Couleurs now : "+couleur1+" "+couleur2);
            if (couleur1.equals("noir")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.black);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.black);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.black);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.black);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.black);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.black);
                }
            }
            else if (couleur1.equals("blanc")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.white);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.white);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.white);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.white);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.white);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.white);
                }
            }
            else if (couleur1.equals("orange")) {
                if (couleur2.equals("white")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.orange);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.orange);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.orange);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.orange);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.orange);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.orange);
                }
            } 
            if (couleur1.equals("jaune")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.yellow);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.yellow);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.yellow);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.yellow);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.yellow);
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.yellow);
                }
            }
            if (couleur1.equals("rouge")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.red.darker());
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.red.darker());
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.red.darker());
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.red.darker());
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.red.darker());
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.red.darker());
                }
            }    
            if (couleur1.equals("vert")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.green.darker());
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.green.darker());
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.green.darker());
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.green.darker());
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.green.darker());
                }
                else if (couleur2.equals("bleu")) {
                    taches.conversionGraphics(graphtaches,1,Color.blue,Color.green.darker());
                }
            }    
            if (couleur1.equals("bleu")) {
                if (couleur2.equals("orange")) {
                    taches.conversionGraphics(graphtaches,1,Color.orange,Color.blue);
                }
                else if (couleur2.equals("blanc")) {
                    taches.conversionGraphics(graphtaches,1,Color.white,Color.blue);
                }
                else if (couleur2.equals("jaune")) {
                    taches.conversionGraphics(graphtaches,1,Color.yellow,Color.blue);
                }
                else if (couleur2.equals("noir")) {
                    taches.conversionGraphics(graphtaches,1,Color.black,Color.blue);
                }
                else if (couleur2.equals("vert")) {
                    taches.conversionGraphics(graphtaches,1,Color.green.darker(),Color.blue);
                }
                else if (couleur2.equals("rouge")) {
                    taches.conversionGraphics(graphtaches,1,Color.red.darker(),Color.blue);
                }
            }    
            // Palette de couleur - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            
            
            //out.ajouterString("texteapplet", "Taille caractéristique calculée: "+(float)echelle_tache+" pixels.");       
            out.ajouterDouble("lcnow",echelle_tache);
            
            
            tpsactuel++;

        }
            
        // ----------------------Ici on va faire la fft ---------------------------------
       /* méthode 1
        if(geometrie.equals("queue")){  
            out.ajouter("fft",fft);
        }
        else if (geometrie.equals("corps")){
            
            double[] auxilfft= new double[dimx*dimy];
         
            double[] zero    = new double[dimx*dimy];
	    double[][] taches_conv_fft ;
            taches_conv_fft = taches.conversion(dimx,dimy,1);
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    auxilfft[i* dimx +j]=taches_conv_fft[i][j];
                    zero[i*dimx+j]=0.0;
                }   
            }   
            double[][] resfft = new double[dimy][dimx];
            FFT2d fourier = new FFT2d(auxilfft, zero   ,dimx,dimy);
            double max;
            max=0.0;
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    resfft[i][j]=Math.sqrt((Math.abs(auxilfft[i* dimx +j]))*(Math.abs(auxilfft[i* dimx +j]))+(Math.abs( zero[i*dimx+j]))*(Math.abs( zero[i*dimx+j])));
                    if(resfft[i][j]>max){
                        max=resfft[i][j];
                    }
                }
            }
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    resfft[i][j]=resfft[i][j]*255/max;//ici souci car si quelque chose dépasse beaucoup cela écrase l'échelle de couleurs
                }
            }
            System.out.println("Max fft pour renormalisation : "+max);
            out.ajouter("fft",resfft);
        } fin methode 1*/
     
       //méthode 2 --->
        if(geometrie.equals("queue")){  
            out.ajouter("fft",fft);
            out.ajouterDouble("lcfourier",1.);
            out.ajouter("pulsationspatiale",1.);
            out.ajouter("spectre",1.); 
            out.ajouterString("texteapplet", "Longueur de corrélation : non calculée.    Période spatiale issue de la TF : non calculée.");
        }
        
        else if (geometrie.equals("corps")){
           
            /*double[][] taches_conv_fft ;
            taches_conv_fft = taches.conversion(dimx,dimy,1);
      
            double[][] resfft = new double[dimy][dimx];
            TFLib.transfo2D_FFT( taches_conv_fft, resfft ,true, false);
            double max;
            max=0.0;
 
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                     if(resfft[i][j]>max){
                        max=resfft[i][j];
                    }
                }
            }
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    resfft[i][j]=resfft[i][j]*255/max;//ici souci car si quelque chose dépasse beaucoup cela écrase l'échelle de couleurs
                }
            }
            out.ajouter("fft",resfft);
            
            double lc_by_tf = lc_fft(resfft) ;
            System.out.println("Taille caracteristique a partir de la TF : " + lc_by_tf) ;
            out.ajouterDouble("lcfourier",lc_by_tf);*/
        
            double[][] taches_conv_fft ;
            taches_conv_fft = taches.conversion(dimx,dimy,1);
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    taches_conv_fft[i][j]=taches_conv_fft[i][j]-(double)(somme);
                }
            }
            double[][] resfft = new double[dimy][dimx];
            TFLib.transfo2D_FFT( taches_conv_fft, resfft ,powerlog_bool, true);
            double max;
            double minileyk;            
            max=0.0;
            minileyk=1000000.;
            int iileyk;
            int jileyk;
            iileyk=0;
            jileyk=0;
            
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    if((resfft[i][j]>max) && (i!=dimx/2) && (j!=dimx/2)) {// && (resfft[i][j]<resfft[64][64])){
                        max=resfft[i][j];
                        iileyk=i;
                        jileyk=j;
                    }
                    if((resfft[i][j]<minileyk) && (i!=dimx/2) && (j!=dimx/2)){
                        minileyk=resfft[i][j];
                    }
                }
            }
            
            //System.out.println("Sam et : "+iileyk+" "+jileyk+" "+max+" "+minileyk);
            
            for (int i=0; i<dimy;i++){
                for (int j=0; j<dimx;j++){
                    resfft[i][j]=255.*((resfft[i][j]-minileyk)/(max-minileyk));//resfft[i][j]*(255./max);//255.*((resfft[i][j]-minileyk)/(max-minileyk));//*255/(max/1.);//ici souci car si quelque chose dépasse beaucoup cela écrase l'échelle de couleurs
                }
            }
            
            if (powerlog.equals("logarithmic")){
                resfft[dimx/2][dimx/2]=resfft[dimx/2+1][dimx/2];
            }
            else {
                resfft[dimx/2][dimx/2]=0.;
            }
            //out.ajouter("fft",fft);
            out.ajouter("fft",resfft);
            
            //for (int i=0; i<(dimx/2); i++){
            //System.out.println(i+" "+resfft[i][0]);
            //coupe[i] = fourier_transform[i+(int)(((double)dimx)/4.)][dimx/2] ;
            //}
            
            // ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~   
            
            double[] ring = new double[dimx/2] ;  
            
            int[] ring_sum = new int[dimx/2] ;
            
            for (int i=0; i<dimx; i++){
                for (int j=0; j<dimx; j++){
                    //ring[(int)(Math.sqrt((double)((i-dimx/4)*(i-dimx/4)+(j-dimx/4)*(j-dimx/4)))+1.)]=ring[(int)(Math.sqrt((double)(i*i+j*j))+1.)]+fourier_transform[i+dimx/4][j+dimx/4];
                    //ring_sum[(int)(Math.sqrt((double)((i-dimx/4)*(i-dimx/4)+(j-dimx/4)*(j-dimx/4)))+1.)]=ring_sum[(int)(Math.sqrt((double)(i*i+j*j))+1.)]+1;
                    if ((int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))<dimx/2) {
                        //System.out.println((int)(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2)))+1.)+" "+fourier_transform[i+dimx/2][j+dimx/2]);
                        //System.out.println((int)(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))+" "+i+" "+j+" 63");
                        ring[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]=ring[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]+resfft[i][j];
                        ring_sum[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]=ring_sum[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]+1;
                    }
                }
            }
            
            for (int i=0; i<dimx/2; i++){  
                ring[i]=ring[i]/(double)ring_sum[i];
                //System.out.println(i+" "+ring_sum[i]);
            }
            
            for (int i=0; i<dimx/2; i++){
                sizeileyk[i]=(double)(i);//((double)dimx)/4.+(double)i;
                fftileyk[i]=ring[i];//resfft[i+(int)(((double)dimx)/4.)][dimx/2];//ring[i];//resfft[i+(int)(((double)dimx)/4.)][dimx/2];
                //System.out.println("ileyk : "+sizeileyk[i]+" "+fftileyk[i]);
                out.ajouter("pulsationspatiale",sizeileyk[i]);
                out.ajouter("spectre",fftileyk[i]); 
                //System.out.println((double)i+" "+fftileyk[i]);
            }
            //out.ajouter("sizeileyk",sizeileyk);
            //out.ajouter("fftileyk",fftileyk);
            
            
            // ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
            double lc_by_tf = lc_fft(resfft) ;
            //System.out.println("Taille caracteristique a partir de la TF : " + lc_by_tf) ;
            out.ajouterDouble("lcfourier",lc_by_tf);
            out.ajouterString("texteapplet", "Longueur de corrélation : "+Math.round(echelle_tache)+" pixels.    Période spatiale issue de la TF : "+Math.round(lc_by_tf)+" pixels.");
        
        }
        //out.ajouter("fft",fft);

        return out;
    }

    /** 
     * Méthode qui fait évoluer la grille courante
     * @param i
     * Indice de la cellule qui va évoluer
     * @param grilleold
     * Grille qui va évoluer
     * @param rr1
     * Rayon d'action de l'activateur
     * @param rr2
     * Rayon d'action de l'inhibiteur
     * @param jj1
     * Coefficient de diffusion de l'activateur
     * @param jj2
     * Coefficient de diffusion de l'inhibiteur
     * @param hh
     * Valeur du palier
     */
    public void evolution_grille_asynchrone(int i,Grille grilleold,double rr1,double rr2,double jj1,double jj2,double hh)
    {  
        int nbcellx;
        int nbvoisinscell1;
        //int nbcell;
        //nbcellx=grilleold.getNombreLigne();
        //nbcell=nbcellx*nbcellx;
        double nlig;
        double ncol;
        //declarer le type d'objets dans le vecteur
        Vector<Cellule> voisins1;
        Cellule cellule1;
        Cellule cellule2;
        double sumi;
        
        //Actualisation de l'etat des cellules (i) une par une
    
        //System.out.println("debut de la boucle sur toute la grille");
        // System.out.println("nbcell"+(nbcell));
         
            
        // System.out.println("coucou");
        // System.out.println("i en cours-actualisation grille : "+i);
        sumi=0.+hh;
        cellule1=grilleold.getCellule(i);
        voisins1=cellule1.getVoisins();
        nbvoisinscell1=voisins1.size();
            
        for (int j=0; j<nbvoisinscell1;j++){
            Cellule voisinactuel;
            voisinactuel = voisins1.elementAt(j);

            //Ajout du terme correspondant a j2:
            if (  (grilleold.distance(cellule1,voisinactuel)>=rr1)&& (grilleold.distance(cellule1,voisinactuel)<rr2)  ){
                   
                if (voisinactuel.statut()){
                    sumi=sumi+jj2;
                    }
                else{
                    sumi=sumi-jj2;
                }
            }
            //
            //Ajout du terme correspondant a j1:
		    else{ 
                if (grilleold.distance(cellule1,voisinactuel)< rr1){
                    if (voisinactuel.statut()){
                        sumi=sumi+jj1;
                    }
                    else{
                        sumi=sumi-jj1;
                    }
                }
            }  
        } 

        if (sumi>0){
            if(((grilleold.getCellule(i)).statut())==false){
                (grilleold.getCellule(i)).changementStatut();                
            }
        }
        else{
            if(((grilleold.getCellule(i)).statut())==true){
                (grilleold.getCellule(i)).changementStatut();
            }
        }
        //System.out.println("J2= "+jj2);
        //System.out.println("sumi"+sumi+"pour i"+i);      
    }
    /*
    public void onde_plane(boolean defilement_arg, int f_zoom_arg) {
    }
    public ListeValeurs calcul(ListeValeurs in) throws SimuException {
    }
    public void initParamIn(ListeValeurs in) throws SimuException{
    }
    */


    //===========================================Début Fonction de Correlation===========================================
    /** 
     * Méthode qui permet, à partir d'une grille contenant des taches, de déterminer la somme normalisée de cellules activées
     * pour chaque taille de carré d'échantillonnage. En d'autres termes, elle calcule la fonction de corrélation de l'image.
     * Les carrés d'échantillonnage ont des tailles variant de 1 pixel à la moitié de la dimension de la grille considérée. Ils
     * balayent ensuite la grille entièrement en laissant une petite partie non exploitée correspondant au fait que le nombre de
     * carrés juxtaposés n'atteint pas forcément exactement à la taille de la grille.
     * @param taches1
     * L'image contenant des taches dont on cherche à déterminer la fonction de corrélation (matrice de réels).
     * Les cellules activées correspondent aux points d'intensité strictement positive.
     * @return sommation
     * La valeur de la somme normalisée en fonction de la taille de carré = fonction de corrélation de l'image (tableau de réels).
     */
    //public double[] correlation (GrilleCarree taches1){
    public double[] correlation (double[][] taches1){ // On accepte maintenant tout type de grille pré-convertie en matrice 2D
            
        int rayon_max = Math.min(dimx,dimy)/2 ;
        int rayon_min = 1 ;
        int pas = 1 ; // ATTENTION : dans les méthodes qui suivent, le pas est supposé de 1... 
        
        double somme_cell_k ;
        int nb_sum = (int)((double)(rayon_max-rayon_min)/(double)(pas)) ; // Attention : relation entre rmax, rmin et pas !
        double[] sommation = new double[rayon_max] ; // Tableau somme des "carrés" en fonction de leur taille
        
        for (int k=rayon_min; k<rayon_max; k=k+pas){ // On fait grossir le carré
            somme_cell_k = 0 ; // Réinitialisation de la somme des cellules à chaque changement de taille
            
            // Détection des cellules appartenant au carré de dimension k*k (initialisation)
            double[][] carre_cellules = new double[k][k] ;
            int nb_carres = (int)(((double)(dimx/k))*((double)(dimy/k))) ;
            double[] somme_bis = new double[nb_carres] ;
            
            int index = 0 ; // Indice du carré
            
            for (int i_k=0; i_k<(dimx/k)*k; i_k += k){ // Déplacement du carré de sa taille (translation du carré initial)
                for (int j_k=0; j_k<(dimy/k)*k; j_k += k){
                    
                    for (int ii=0; ii<k; ii++){ // Remplissage des cellules de la grille dans le carré créé
                        for (int jj=0; jj<k; jj++){
                            //if ( (taches1.getCellule(i_k + ii, j_k + jj)).statut() ){ // Modification suite à la conversion en matrice 2D
                            if ( taches1[i_k + ii][j_k + jj] > 0 ){
                                carre_cellules[ii][jj] = 1 ;
                            }
                            else {
                                carre_cellules[ii][jj] = -1 ;
                            }
                        }
                    }
                    
                    somme_cell_k = 0 ; // Réinitialisation de la somme des cellules à chaque déplacement du carré
                    // Faire la sommation sur tous les éléments
                    for (int ii=0; ii<k; ii++){
                        for (int jj=0; jj<k; jj++){
                            somme_cell_k += carre_cellules[ii][jj] ; 
                        }
                    }
                    somme_bis[index] = Math.abs(somme_cell_k) / (double)(k*k) ;
                    index += 1 ;
                }
            } // Fin boucle déplacement sur la grille
            
            double moyenne = 0 ;
            for (int i=0; i<index; i++){
                moyenne += somme_bis[i] ;  
            }
            moyenne = moyenne / (double)(nb_carres) ; // (double)(index) ;
            //sommation[ (int)((double)(k)/(double)(rayon_min)) - 1 ] = moyenne ;
            sommation[k] = moyenne ;
            
        } // Fin boucle sur k : la taille des carrés	
        
        return sommation; 
    } //===========================================Fin Fonction de Correlation===========================================
    
    
    //===========================================Début Dérivée d'une Fonction===========================================
    /** 
     * Méthode qui permet d'obtenir la dérivée d'une fonction. Attention, cette méthode est une approximation de la dérivée,
     * elle calcule la pente entre deux points succesifs.
     * @param fonction
     * La fonction que l'on cherche à dériver (tableau de réels).
     * @return derivation
     * La dérivée de la fonction (tableaux de réels).
     */
    public double[] derivee (double[] fonction){    
        
        // Lire la taille du tableau de la fonction à dériver
        int nb_elements = fonction.length ;
        int pas = 1 ; // Egal au pas de la méthode taille caractéristique dans ce cas... sortir les arguments de la méthode ?
        int rayon_min = 1 ;
        
        // Abscisse de la fonction
        double[] taille_carre = new double[nb_elements] ;
        for (int i=0; i<nb_elements; i++){ // Remplissage du vecteur taille de carré
            taille_carre[i] = rayon_min + pas*(i+1) ; 
        }
        
        double[] derivation = new double[nb_elements] ; // On s'interesse à la valeur entre deux tailles de carré : nb_elements-1 <===== A VERIFIER
        derivation[0] = 0 ; // Valeur ajoutée pour le test de la derivée
        for (int i=1; i<nb_elements-1; i++){ // Calcul de la dérivée
            derivation[i] = ( (double)(fonction[i+1]-fonction[i])/(double)(taille_carre[i+1] - taille_carre[i]) ) ;
        }
        
        return derivation ; 
    } //===========================================Fin Dérivée d'une Fonction===========================================
    

    //===========================================Début Moindres Carrés Linéaires=========================================== 
    /** 
     * Méthode servant à déterminer un ajustement linéaire sur un set de points expérimentaux via la méthode des moindres carrés.
     * @param x_exp
     * Les abscisses des points expérimentaux (tableau de réels).
     * @param y_exp
     * Les ordonnées des points expérimentaux (tableau de réels).
     * @return coeff_lms
     * coeff[0] contient la valeur du coefficient directeur de l'ajustement linéaire (réel).
     * coeff[1] contient la valeur de l'orodonnées à l'origine de l'ajustement linéaire (réel).
     */
    public double[] least_mean_square (double[] x_exp, double[] y_exp) {
        
        // Détermination du nombre de points expérimentaux
        int N = x_exp.length ;
        double [] coeff_lms = new double[2] ; // Tableau de taille 2 où l'on rentre les coefficients
        
        // Initialisation des sommes pour le calcul des coefficients
        double xsum =0. ;
        double ysum =0. ;
        double xysum =0. ;
        double xxsum =0. ;
        
        // Somme sur tous les éléments
        for (int i=0; i<N; i++){
            xsum += x_exp[i] ;
            ysum += y_exp[i] ;
            xysum += (x_exp[i])*(y_exp[i]) ;
            xxsum += (x_exp[i])*(x_exp[i]) ;
        } 
        
        // Calcul des coefficients
        coeff_lms[0] = ( N*xysum - xsum*ysum ) / ( N*xxsum - xsum*xsum ) ; // Coeff Directeur
        coeff_lms[1] = ( ysum*xxsum - xsum*xysum ) / ( N*xxsum - xsum*xsum ) ; // Ordonnée à l'origine
        
        return coeff_lms ;
    }//===========================================Fin Moindres Carrés Linéaires=========================================== 
    
    
    //===========================================Début Taille Caractéristique===========================================
    /** 
     * Première méthode pour déterminer la taille caractéristique des taches observées.
     * Cette méthode recherche le point où la dérivée de la fonction de corrélation s'annule ce qui donne la taille cracatérisitque
     * en première approximation. Ensuite, un ajustement linéaire est réalisé sur les valeurs comprises entre x=0 et x=l'approximation.
     * Ensuite une moyenne est réalisée sur le deuxième set de points (de l'approximation à la fin de la série), elle nous donne l'ordonnée
     * à l'origine d'une fonction affine constante. L'intersection entre ces deux droites est la taille cractéristique de
     * l'image plus précise.
     * @param fct_correlation
     * La fonction de corrélation (tableau de réels) sur laquelle on se base pour calculer la taille cractéristique.
     * @param deriv_correl
     * La dérivée de la fonction de corrélation (tableau de réels) utilisée pour déterminer la taille cracatéristique en première approximation.
     * @return taille_carac
     * La taille cractéristique (réel) des taches présentes sur l'image.
     */ 
    public double taille_caracteristique (double[] fct_correlation, double[] deriv_correl){ //double[] x_corrsum double fct_sum
    
        double taille_carac = 0. ;
        int N = fct_correlation.length ; 
        int marge_erreur = 1 ;
        
        // Condition sur la dérivée : elle passe par 0
        int indice = 1 ; // Initialisation de l'indice servant à une première approximation de la taille carac
        for (int j=1; j<N; j++) { // On récupère le point où la dérivée s'annule
            if ( Math.abs(deriv_correl[j]) < 0.01 ) {
                indice = j ;
                break;
            }
        }     
        
        if ( (indice - marge_erreur > 2) && (N - indice - marge_erreur > 2) ) { // Pour que les moindres carrés aient un sens
            double[] x_exp1 = new double[indice - marge_erreur - 1] ; // Création des tableaux correspondant au nombre de points considérés
            double[] y_exp1 = new double[indice - marge_erreur - 1] ;
            double[] x_exp2 = new double[N - indice - marge_erreur] ;
            double[] y_exp2 = new double[N - indice - marge_erreur] ;
        
            // Moindres carrés sur [0, indice]
            for (int i=1; i<indice - marge_erreur; i++){
                y_exp1[i-1] = fct_correlation[i] ;
                x_exp1[i-1] = i ;
            }
            double coeff1[] ;
            coeff1 = least_mean_square(x_exp1, y_exp1) ;
            double coeff2_av;
            double coeff2_new;
            coeff2_av=0.;
            // Moindres carrés sur [indice, +infty]
            for (int i=indice+marge_erreur; i<N; i++){
                y_exp2[i-indice-marge_erreur] = fct_correlation[i] ; 
                x_exp2[i-indice-marge_erreur] = i ;
                coeff2_av=coeff2_av+y_exp2[i-indice-marge_erreur];
            }
            
            //double coeff2[] ;
            
            //for (int i=1; i<indice - marge_erreur; i++){
            coeff2_new=coeff2_av/(double)(N-(indice+marge_erreur)+1);
            //}
            
            //coeff2 = least_mean_square(x_exp2, y_exp2) ;
            
            //coeff2[0]=0.;
            
            // Point d'intersection = taille cractéristique
            taille_carac = (coeff2_new - coeff1[1]) / coeff1[0] ;
        }
        return taille_carac ;
    }//===========================================Fin Taille Caractéristique=========================================== 


    //===========================================Début Taille Caractéristique à partir de la FFT===========================================
    /**
     * Méthode qui calcule la taille caractéristique des taches à partir de la transformée de Fourier de l'image des taches.
     * Elle détermine la distance entre le maximum de la TF et le second maximum. Pour cela, cette méthode calcule des moyennes
     * entre les points de la transformées de Fourier compris dans des anneaux situés à une distance déterminée de l'origine de la TF. 
     * @param fourier_transform
     * La transformée de Fourier de l'image des taches (tableau 2D de réels).
     * @return taille_carac
     * La taille caractéristique ainsi déterminée (réel).
     */
    public double lc_fft (double[][] fourier_transform){
        
        /*double[] coupe = new double[dimx/2] ; // Vecteur dans lequel on rentre une coupe de la TF
        for (int i=0; i<dimx/2; i++){
            coupe[i] = fourier_transform[i][0] ;
        }*/
        
        double[] coupe = new double[dimx/2] ; // Vecteur dans lequel on rentre une coupe de la TF
        
        //double[][] coupe_av = new double[dimx/2][dimx/2] ; // Vecteur dans lequel on rentre une coupe de la TF   
        
        double[] ring = new double[dimx/2] ;  
        
        int[] ring_sum = new int[dimx/2] ;
        
        // ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
        
        /*for (int i=0; i<dimx/2; i++){
         //System.out.println(i+" "+fourier_transform[i]);
         coupe[i] = fourier_transform[i+(int)(((double)dimx)/4.)][dimx/2] ;
         }*/
        
        
        // -----
        for (int i=0; i<dimx; i++){
            for (int j=0; j<dimx; j++){
                //ring[(int)(Math.sqrt((double)((i-dimx/4)*(i-dimx/4)+(j-dimx/4)*(j-dimx/4)))+1.)]=ring[(int)(Math.sqrt((double)(i*i+j*j))+1.)]+fourier_transform[i+dimx/4][j+dimx/4];
                //ring_sum[(int)(Math.sqrt((double)((i-dimx/4)*(i-dimx/4)+(j-dimx/4)*(j-dimx/4)))+1.)]=ring_sum[(int)(Math.sqrt((double)(i*i+j*j))+1.)]+1;
                if ((int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))<dimx/2) {
                    //System.out.println((int)(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2)))+1.)+" "+fourier_transform[i+dimx/2][j+dimx/2]);
                    //System.out.println((int)(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))+" "+i+" "+j+" 63");
                    ring[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]=ring[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]+fourier_transform[i][j];
                    ring_sum[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]=ring_sum[(int)Math.ceil(Math.sqrt((double)((i-dimx/2)*(i-dimx/2)+(j-dimx/2)*(j-dimx/2))))]+1;
                }
            }
        }
        
        for (int i=0; i<dimx/2; i++){  
            coupe[i]=ring[i]/(double)ring_sum[i];
        }

        
        /*
                
        // On détermine le maximum de la coupe de la TF (normalement vers 0...)
        double max_fft = 0. ;
        int max_fft_indice1 = 0 ;
        for (int i=0; i<dimx/2; i++){
            if (coupe[i] > max_fft){
                max_fft = coupe[i] ;
                max_fft_indice1 = i ;
            }
        }
        //System.out.println("Indice max FFT : " + max_fft_indice) ;
        
        
        // On détermine le premier minimum de la coupe de la TF <===================== PROBLEME
        //double[] derivee_fft = derivee(coupe) ;
        
        for (int i=0; i<dimx/2; i++){
            System.out.println(i + " " + coupe[i]) ;
        }
        
        int min_fft_indice = 0 ;
        
        for (int i=0; i<derivee_fft.length; i++){
            if (Math.abs(derivee_fft[i]) < 0.1){
                min_fft_indice = i ;
            }
        }                               
        
        
        double min_fft = max_fft ;
        int[] min_fft_indice = new int[coupe.length] ;
        int[] max_fft_indice = new int[coupe.length] ;
        int Ind_min = 0 ;
        int Ind_max = 0 ;
        //int min_fft_indice = 0 ;
        for (int i=0; i<dimx/2-1; i++){
            if ( (coupe[i] < max_fft) && (coupe[i] < coupe[i+1]) ){
                min_fft = coupe[i] ;
                min_fft_indice[Ind_min] = i ; // On récupère tous les minima locaux
                Ind_min += 1 ;
                System.out.println("Minimul local : " + i) ;
                //min_fft_indice = i ;
                //break ;
            }
            if ( (coupe[i] > min_fft) && (coupe[i] > coupe[i+1]) ){
                max_fft = coupe[i] ;
                max_fft_indice[Ind_max] = i ; // On récupère les maxima locaux
                Ind_max += 1 ;
            }
        }
        // On fait la moyenne de tous les écarts entre les minima locaux
        int somme_ecart = 0 ;
        for (int i=0; i<Ind_min-1; i++){
            somme_ecart += Math.abs(min_fft_indice[i] - min_fft_indice[i+1]);
        }
        double moyenne_ecarts = ( (double)(somme_ecart) ) / ( (double)(Ind_min) ) ; 
        System.out.println("moyenne : " + moyenne_ecarts) ;
        
        double[] somme = new double[dimx/2] ;
        for (int i=0; i<dimx/2; i++){
            for (int j=0; j<dimy/2; j++){
                somme[i] += fourier_transform[i][j] ;
            }
            System.out.println(i + " " + somme[i]) ;
        }
        
        
        //System.out.println("Indice min FFT : " + min_fft_indice) ;
        
        // La taille cractéristique correspond à la distance entre le max et le min
        double taille_carac = (4*Math.PI) / moyenne_ecarts ; //Math.abs(max_fft_indice - min_fft_indice);
        */
        
        
        // On détermine le maximum de la coupe de la TF (normalement vers 0...)
        double max_fft = 0. ;
        int max_fft_indice1 = 0 ;
        for (int i=1; i<dimx/2; i++){
            if (coupe[i] > max_fft){
                max_fft = coupe[i] ;
                max_fft_indice1 = i ;
                //System.out.println("plouf : " + max_fft_indice1+" "+max_fft) ;
            }
        }
        //System.out.println("Indice max FFT : " + max_fft_indice1) ;
        
        // La taille cractéristique correspond à la distance entre le max et le min
        double taille_carac = ((double)dimx)/((double)max_fft_indice1);
        
        return taille_carac ;
    }//===========================================Début Taille Caractéristique à partir de la FFT===========================================
    
    


    // ------------------------------------------------------------------------------------------
    /** 
     * Méthode qui fait évoluer la grille courante de facon synchrone
     * @param i
     * Indice de la cellule qui va évoluer
     * @param grilleold
     * Grille qui ne va pas évoluer
     * @param grille
     * Grille qui va évoluer
     * @param rr1
     * Rayon d'action de l'activateur
     * @param rr2
     * Rayon d'action de l'inhibiteur
     * @param jj1
     * Coefficient de diffusion de l'activateur
     * @param jj2
     * Coefficient de diffusion de l'inhibiteur
     * @param hh
     * Valeur du palier
     */
    public void evolution_grille_synchrone(int i,Grille grilleold,Grille grille,double rr1,double rr2,double jj1,double jj2,double hh)
    {  
        int nbcellx;
        int nbvoisinscell1;
        //int nbcell;
        //nbcellx=grilleold.getNombreLigne();
        //nbcell=nbcellx*nbcellx;
        double nlig;
        double ncol;
        //declarer le type d'objets dans le vecteur
        Vector<Cellule> voisins1;
        Cellule cellule1;
        Cellule cellule2;
         double sumi;
       
        //Actualisation de l'etat des cellules (i) une par une
        // On les cree dans grillenew
    
        //System.out.println("debut de la boucle sur toute la grille");
        // System.out.println("nbcell"+(nbcell));
         
            
        // System.out.println("coucou");
        // System.out.println("i en cours-actualisation grille : "+i);
        sumi=0.+hh;
        cellule1=grilleold.getCellule(i);
        voisins1=cellule1.getVoisins();
        nbvoisinscell1=voisins1.size();
            
        for (int j=0; j<nbvoisinscell1;j++){
      
            Cellule voisinactuel;
            voisinactuel = voisins1.elementAt(j);

            //Ajout du terme correspondant a j2:
            if ((grilleold.distance(cellule1,voisinactuel)>=rr1)&&(grilleold.distance(cellule1,voisinactuel)<rr2)){
                   
                if (voisinactuel.statut()){
                    sumi=sumi+jj2;
                }
                else{
                    sumi=sumi-jj2;
                }
            }
            //
            //Ajout du terme correspondant a j1:
            else{
                if(grilleold.distance(cellule1,voisinactuel)<rr1){
                    if (voisinactuel.statut()){
                        sumi=sumi+jj1;
                    }
                    else{
                        sumi=sumi-jj1;
                    }
                }
            }	    
        } 

        if (sumi>0){
            if(((grilleold.getCellule(i)).statut())==false){
                (grille.getCellule(i)).changementStatut(); // !!!!!!!!!!!!!!                
            }
        }
        else{
            if(((grilleold.getCellule(i)).statut())==true){
                (grille.getCellule(i)).changementStatut();// !!!!!!!!!!!!!!
            }
        }
        //System.out.println("J2= "+jj2);
        //System.out.println("sumi"+sumi+"pour i"+i);       
    }

    // ------------------------------------------------------------------------------------------
}


