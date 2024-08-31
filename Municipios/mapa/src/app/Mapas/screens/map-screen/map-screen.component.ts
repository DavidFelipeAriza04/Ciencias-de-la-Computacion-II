import { Component, AfterViewInit } from '@angular/core';
import * as L from 'leaflet'

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
    // Coordenadas de Bogotá y Medellín
    const bogotaCoords: L.LatLngExpression = [4.6097, -74.0817];
    const medellinCoords: L.LatLngExpression = [6.2442, -75.5812];

    // Trazar la línea entre Bogotá y Medellín
    const latlngs: L.LatLngExpression[] = [bogotaCoords, medellinCoords];

    const polyline = L.polyline(latlngs, { color: 'blue' }).addTo(this.map);

    // Ajustar el mapa para que la línea se vea completamente
    this.map.fitBounds(polyline.getBounds());
  }
}
