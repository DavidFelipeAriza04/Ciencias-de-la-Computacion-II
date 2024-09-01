import { Component, AfterViewInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import * as L from 'leaflet'

const url = "http://127.0.0.1:8000/"
@Component({
  selector: 'app-map-screen',
  standalone: true,
  imports: [],
  templateUrl: './map-screen.component.html',
  styleUrl: './map-screen.component.css'
})
export class MapScreenComponent implements AfterViewInit{

  private map!:L.Map;

  private initMap(): void {
    this.map = L.map('map', {
      center: [ 39.8282, -98.5795 ],
      zoom: 3
    });

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);
  }

  constructor(){}

  ngAfterViewInit(): void {
    this.initMap();
    this.drawLine();
  }

  private drawLine(): void {
    // Coordenadas de los municipios 
    fetch(url + "Municipios/")
    .then(response => response.json())
    .then(data => {
      data.forEach((municipio: any) => {
        const coords: L.LatLngExpression = [municipio["latitud"], municipio["longitud"]];
        L.marker(coords, {
          title: municipio["nombre"],
          alt: municipio["nombre"],
          riseOnHover: true
        }).addTo(this.map)
      })
    })
    .catch(error => console.log(error))
    const bogotaCoords: L.LatLngExpression = [4.6097, -74.0817];
    const medellinCoords: L.LatLngExpression = [6.2442, -75.5812];

    // Trazar la línea entre Bogotá y Medellín
    const latlngs: L.LatLngExpression[] = [bogotaCoords, medellinCoords];

    const polyline = L.polyline(latlngs, { color: 'blue' }).addTo(this.map);

    // Ajustar el mapa para que la línea se vea completamente
    this.map.fitBounds(polyline.getBounds());
  }

  
}
