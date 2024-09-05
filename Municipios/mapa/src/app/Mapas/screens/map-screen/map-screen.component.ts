import { Component, AfterViewInit, Output, effect, inject } from '@angular/core';
import { Title } from '@angular/platform-browser';
import * as L from 'leaflet';
import { MapaService } from '../../services/mapa.service';
import { Municipio } from '../../interfaces/Municipio.interface';

const url = 'http://127.0.0.1:8000/';
@Component({
  selector: 'app-map-screen',
  standalone: true,
  imports: [],
  templateUrl: './map-screen.component.html',
  styleUrl: './map-screen.component.css',
})
export class MapScreenComponent implements AfterViewInit {
  private mapaService = inject(MapaService);
  private map!: L.Map;
  private municipios!: Municipio[];
  private grafo: L.Polyline[] = []; // Inicializa grafo como un array vacío
  private recorridoMapa: L.Polyline[] = [];

  @Output()
  origenYdestino: String[] = ['', ''];

  origen: boolean = true;

  icon = L.icon({
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    iconUrl: 'assets/images/marker-icon.png',
    shadowUrl: 'assets/images/marker-shadow.png',
  });

  constructor() {
    // Inicializa el efecto cuando el componente se inicializa
    effect(() => {
      const recorrido = this.mapaService.recorrido();
      if (recorrido.length > 0) {
        this.dibujarRecorrido();
      }
    });
  }

  ngAfterViewInit(): void {
    this.initMap();
    this.mapaService.get_municipios().subscribe({
      next: (resData) => {
        this.municipios = resData;
        this.mapaService.set_municipios_service(resData);
        this.drawMarkers();
        this.drawLines();
      },
      error: (err) => {
        console.log(err);
      },
    });
  }

  private initMap(): void {
    this.map = L.map('map', {
      center: [5.387499, -74.132269],
      zoom: 6,
    });

    const tiles = L.tileLayer(
      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        maxZoom: 18,
        minZoom: 3,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }
    );

    tiles.addTo(this.map);
  }

  private drawMarkers(): void {
    this.municipios.forEach((municipio) => {
      L.marker([municipio.latitud, municipio.longitud], {
        title: municipio.nombre,
        alt: municipio.nombre,
        riseOnHover: true,
        icon: this.icon, // Aquí pasamos directamente el icono
      })
        .addTo(this.map)
        .on('click', () => this.onMarkerClick(municipio.nombre)) // Llama a la función de Angular
        .bindPopup(municipio.nombre);
    });
  }

  private onMarkerClick(municipio_nombre: string): void {
    if (this.origen) {
      this.origenYdestino[0] = municipio_nombre; // Setea el valor del primer input (origen)
      this.origen = false;
    } else {
      this.origenYdestino[1] = municipio_nombre; // Setea el valor del segundo input (destino)
      this.origen = true;
    }

    this.mapaService.setOrigenYDestino(this.origenYdestino);
  }

  private drawLines(): void {
    let contador = 0;
    this.municipios.forEach((municipio) => {
      for (let i = contador; i < 30; i++) {
        if (
          municipio[
            this.municipios[i]['nombre'].replaceAll(' ', '') + 'Conexion'
          ] != 0
        ) {
          let linea = L.polyline([
            [municipio['latitud'], municipio['longitud']],
            [this.municipios[i]['latitud'], this.municipios[i]['longitud']],
          ]).addTo(this.map);
          this.grafo.push(linea);
        }
      }
      contador++;
    });
  }

  private dibujarRecorrido() {
    console.log(this.mapaService.recorrido());
    if (this.mapaService.recorrido().length == 0) return;
    console.log('Hs');
    for (let i = 0; i < this.mapaService.recorrido().length; i++) {
      if (i != this.mapaService.recorrido().length - 1) {
        let municipio1: Municipio | undefined =
          this.mapaService.municipios_sevice.find(
            (municipio) =>
              municipio['nombre'] ===
              this.mapaService.recorrido()[i].replaceAll('_', ' ')
          );

        let municipio2: Municipio | undefined =
          this.mapaService.municipios_sevice.find(
            (municipio) =>
              municipio['nombre'] ===
              this.mapaService.recorrido()[i + 1].replaceAll('_', ' ')
          );

        if (municipio1 && municipio2) {
          let linea = L.polyline(
            [
              [municipio1['latitud'], municipio1['longitud']],
              [municipio2['latitud'], municipio2['longitud']],
            ],
            { color: 'red' }
          ).addTo(this.map);
          this.recorridoMapa.push(linea);
        }
      }
    }
  }
}
