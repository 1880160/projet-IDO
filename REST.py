# faite par Rodney

from flask import Flask, jsonify, request


try:
    app = Flask(__name__)

    @app.route('/donnees',methods=['GET'])
    def info_donnees():
        return jsonify(
            {
                # "t": int(currentTemp), 
                # "h": int(currentHumid)
            }
        )
    
    @app.route('/etat', methods=['POST'])
    def set_etat():
        if request.method == "POST":
            json = request.get_json()
            if "etat" in json:
                if json["etat"] == 0:
# 0 désactive l’envoi de données, 1 active l’envoi de données
# flag
                    return 1


                elif json["etat"] == 1:
# T(int) : Nombre entier correspondant à la dernière température lue
# H(int) : Nombre entier de 0 à 100 correspondant à la dernière valeur d’humidité lue

                    return 1



                
                return jsonify({'Etat': json["etat"]}),200
        else:
            return jsonify({'Erreur': 'Requetes POST seulement'}),500

    if __name__ == '__main__':
        app.run(host='0.0.0.0',port=3000)


except KeyboardInterrupt:
    print("terminer")