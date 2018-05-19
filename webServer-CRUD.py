from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import CRUDwithWebsite
import cgi
import os

#Request handler class
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                restaurants = CRUDwithWebsite.getAllRestaurants();
                output = ""
                output += "<html><body>Hello!  "
                output += "<a href = '/restaurants/new'>Add a new Restaurant</a>"
                
                for restaurant in restaurants:
                    output += "<p>" + restaurant.name + "</p>"
                    output += "<a href = '/restaurants/"+ str(restaurant.id)+"/edit'>edit</a></br>"
                    output += "<a href = '/restaurants/"+ str(restaurant.id)+"/delete'>delete</a></br>"
                    
                output += "</body></html>"                
                self.wfile.write(output)
                print output
                return            

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"            
                output += """<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>
                           <h2>Add a new restaurant </h2><input name = 'message' type = 'text'><input type = 'submit'></form>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output
                
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()

                #os.path.basename returns the tail of path.split
                #os.path.dirname returns the dir path till the parent directory
                #to fetch restaurant id from restaurants/id/edit, fetch the parent path for the /edit and then fetch the tail
                restaurantId = int(os.path.basename(os.path.dirname(self.path)))

                restaurantName = CRUDwithWebsite.getRestaurant(restaurantId)
                
                output = ""
                output += "<html><body>"
                output += """<form method = 'POST' enctype='multipart/form-data' action='/restaurants/""" + str(restaurantId) + """/edit'>
                          <h2>Edit restaurant: """ + restaurantName + """</h2><input name = 'message' type = 'text'><input type = 'submit'></form>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output        

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurantId = os.path.basename(os.path.dirname(self.path))
                restaurantName = CRUDwithWebsite.getRestaurant(restaurantId)
                
                output = ""
                output += "<html><body>"
                output += "<h2>Delete the restaurant:%s??</h2>" %restaurantName
                output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" %restaurantId
                output += "<input type = 'submit' value = 'Delete'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                
        except IOError:
            self.send_error(404, "File Not Found %s" %self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                self.end_headers()
                
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                #Call the function addRestaurant in CRUDwithWebsite, to add the new restaurant to the database
                CRUDwithWebsite.addRestaurant(messagecontent[0])
                
                output = ""
                output += "<html><body>"
                output += "<h1> %s successfully added </h1>" % messagecontent[0]
                output += "<a href = '/restaurants'>Back to list of Restaurants</a>"

                output += """<form method = 'POST' enctype='multipart/form-data' action='/restaurant/new'>
                           <h2>Add a new restaurant </h2><input name = 'message' type = 'text'><input type = 'submit'></form>"""
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/edit"):
                self.send_response(301)
                self.end_headers()

                #fetch the restaurant id from the path
                restaurantId = int(os.path.basename(os.path.dirname(self.path)))
                                
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    restaurantNewName = fields.get('message')
                    
                CRUDwithWebsite.editRestaurant(restaurantId,restaurantNewName[0])

                output = ""
                output += "<html><body>"
                output += "<h1> %s successfully updated </h1>" % restaurantNewName[0]
                output += "<a href = '/restaurants'>Back to list of Restaurants</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output

            if self.path.endswith("/delete"):                
                #fetch the restaurant id from the path
                restaurantId = os.path.basename(os.path.dirname(self.path))

                #invoke the delete function 
                CRUDwithWebsite.deleteRestaurant(restaurantId)
                
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
                
        except:
            self.send_error(404, "File Not Found %s" %self.path)
                
#entry point of code
def main():
    try:
        #create an instance of the HTTP Server class
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        
        print "Web serverrunning onport %s" %port
        server.serve_forever()

    except KeyboardInterrupt:
        #this interruptkeyboard interrupt is the builtin exception on python, when user holds ctrl+c
        print "^C entered, stopping web server..."
        server.socket.close()


# the following code should be written at the End of file
# This is added to immediately run the main menthod, when the python interpreter executes the script

if __name__ == '__main__':
    main()
    
