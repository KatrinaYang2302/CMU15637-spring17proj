package getdata;

import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;

import javax.xml.parsers.DocumentBuilder;  
import javax.xml.parsers.DocumentBuilderFactory;  

import org.w3c.dom.*;  


public class Data {
	static FileWriter fwStop, fwRtStop;
	static boolean[] hash = new boolean[100000];
	static String key = "EAhYqnqmHrfXvT8rpmSDkgEbP";
	static String method = "getpatterns";
	static String baseURL = "http://truetime.portauthority.org/bustime/api/v1/";
	public static void processRoute(String route) throws IOException{
		String urlStr = baseURL + method + "?key=" + key + "&rt=" + route;
		URL url = new URL(urlStr);
		Scanner res = new Scanner(url.openStream(), "gb2312");
		FileWriter fw = new FileWriter("tmp" + route + ".xml");
		while(res.hasNext()){
			String s = res.nextLine();
			fw.append(s + "\n");
		}
		fw.close();
		res.close();
	}
	
	public static String getContent(Element e, String desc){
		return e.getElementsByTagName(desc).item(0).getFirstChild().getNodeValue();
	}
	
	public static void parseXML(String route) throws Exception{
		System.out.println(route);
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();  
 
        DocumentBuilder dbBuilder = dbFactory.newDocumentBuilder();  
         
        Document doc = dbBuilder.parse("tmp" + route + ".xml"); 
        
        //Node response = doc.getElementsByTagName("bustime-response").item(0);
        
        NodeList inOutBound = doc.getElementsByTagName("ptr");
        int len = inOutBound.getLength();
        for(int i = 0; i < len; i++){
        	Element e = (Element)inOutBound.item(i);
        	String dir = getContent(e, "rtdir");
        	dir += i;
        	NodeList stops = e.getElementsByTagName("pt");
        	int stopsGs = stops.getLength();
        	for(int j = 0; j < stopsGs; j++){
        		Element stop = (Element)stops.item(j);
        		String type = getContent(stop, "typ");
        		if(!type.equals("S")) continue;
        		String stopIdStr = getContent(stop, "stpid");
        		Integer stopId = Integer.parseInt(stopIdStr);
        		if(!hash[stopId]){
        			hash[stopId] = true;
        			String stopName = getContent(stop, "stpnm");
        			String stopLong = getContent(stop, "lon");
        			String stopLat = getContent(stop, "lat");
        			fwStop.append(stopId.toString() + "," + stopName + "," + stopLong + ","
        					+ stopLat + "\n");
        		}
        		String dist = getContent(stop, "pdist");
        		fwRtStop.append(route + "," + dir + "," + stopId.toString() + "," + dist + "\n");
        	}
        }
        
	}
	
	public static void main(String[] args) throws IOException{
		
		String[] routes = new String[1000];
		int numOfRoutes = 0;
		FileReader fr = new FileReader("routes.csv");
		BufferedReader br = new BufferedReader(fr);
		while(true){
			String line = br.readLine();
			if(line == null) break;
			String buf = "";
			int len = line.length();
			for(int i = 0; i < len; i++){
				char c = line.charAt(i);
				if(c == ',') break;
				buf += c;
			}
			routes[numOfRoutes] = buf;
			numOfRoutes++;
		}
		br.close();
		for(int i = 0; i < numOfRoutes; i++){
			//System.out.println(routes[i]);
		}
		fwStop = new FileWriter("stops.csv");
		fwRtStop = new FileWriter("rt_stop.csv");
		for(int i = 0; i < 100000; i++) {
			hash[i] = false;
		}
		for(int i = 0; i < numOfRoutes; i++){
			try {
				parseXML(routes[i]);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		fwStop.close();
		fwRtStop.close();
	}
}
