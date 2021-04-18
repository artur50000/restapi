from racing_pkg import report
from datetime import datetime
from flask import Flask, request, make_response,Response, jsonify
from dicttoxml import dicttoxml
from flasgger import Swagger


def get_app():

    whole_list = report.load_data("data")
    
    app = Flask(__name__)
    swagger = Swagger(app)
    

    whole_list = report.load_data("data")
    whole_list = sorted(whole_list, key=lambda x: x.Abbreviation)
   

    def make_list(list_process):
        

        json_list = []

        for item in list_process:
            json_dict = {}
            json_dict["Abbreviation"] = item.Abbreviation
            json_dict["Name"] = item.Name
            json_dict["Company"] = item.Company
            json_dict["Start Time"] = str(item.start_time)
            json_dict["End Time"] = str(item.end_time)
            json_dict["Result Time"] = str(item.result_time)

            json_list.append(json_dict)

        return json_list

    list_dicts = make_list(whole_list)
    whole_dict = {}

    for item in list_dicts:
        whole_dict[item["Abbreviation"]] = item

   
    @app.route('/api/v1/report')
    def common():
        """
        This is the report API
        Call this api passing a order and content type parameters
        ---
        produces:
          - application/json
          - application/xml
          
        responses:
         '200':
          description: successfull reponse
             
        parameters:
          - name: order
            in: query 
            type: string
            required: false
          - name: format
            in: query 
            type: string
            required: false 
      
        """

        order = request.args.get('order')
        format_resp = request.args.get('format', default='json')
        
        if order == 'desc':
            whole_list.reverse()

        json_list = make_list(whole_list)
        
        if format_resp == 'xml':
            xml = dicttoxml(json_list)

            return app.response_class(xml, mimetype='application/xml')

        elif format_resp == 'json':
            return jsonify(whole_list)

        else:
            return "please, check your request"


    @app.route('/api/v1/detail')
    def detailed():
        """
        This is the report API
        Call this api passing a order and content type parameters
        ---
        produces:
          - application/json
          - application/xml
          
        responses:
         '200':
          description: successfull reponse
             
        parameters:
          - name: driver_id
            in: query 
            type: string
            required: false
          - name: format
            in: query 
            type: string
            required: false 
      
        """

        driver_id = request.args.get('driver_id')
        format_resp = request.args.get('format',default='json')

        item = whole_dict.get(driver_id)

        if format_resp == 'xml' and driver_id:
            
                if item:
                    xml = dicttoxml(item)
                    return app.response_class(xml, mimetype='application/xml')
                else:
                    return "there is no such driver"
      
        elif format_resp == 'json' and driver_id:
            
                if item:
                   return jsonify(item)
                else:
                    return "there is no such driver"
        else:
            return 'please check your request'

    return app
 
 
if __name__ == '__main__':

    app = get_app()
    
    app.run(debug=True)
