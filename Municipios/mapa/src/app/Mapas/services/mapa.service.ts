import { HttpClient } from '@angular/common/http';
import { inject, Injectable, Signal, signal } from '@angular/core';
import { Municipio } from '../interfaces/Municipio.interface';
import { Observable } from 'rxjs';
import {RecorridoData} from "../interfaces/Recorrido.interface"

@Injectable({
  providedIn: 'root'
})
export class MapaService {

  constructor() { }
  private _httpClient = inject(HttpClient);
  private _url:string = "http://127.0.0.1:8000/"
  origenYDestino:String[] = ["",""]
  municipios_sevice: Municipio[] = [];
  distanciaActual = 0

  private _recorrido = signal<String[]>([]);
    
  get recorrido(): Signal<String[]> {
    return this._recorrido;
  }

  setRecorrido(newRecorrido: String[]): void {
    this._recorrido.set(newRecorrido);
  }
  
  public get_municipios():Observable<Municipio[]>{
    return this._httpClient.get<Municipio[]>(this._url+"Municipios/")
  }

  public setOrigenYDestino(origenYDestino:String[]):void{
    this.origenYDestino = origenYDestino;
  }

  public get_recorrido(origenYDestino: Municipio[], algoritmo: string): Observable<RecorridoData> | null {
    if (origenYDestino[0].nombre !== "" && origenYDestino[1].nombre !== "" && algoritmo !== "") {
      const payload = { origen: origenYDestino[0], destino: origenYDestino[1], algoritmo: algoritmo };
      return this._httpClient.post<RecorridoData>(this._url + "/Municipios/", payload);
    } 
    return null;
  }

  public set_municipios_service(municipios:Municipio[]):void{
    this.municipios_sevice = municipios;
  }

  public buscar_municipio(nombre: string): Municipio {
    const municipio = this.municipios_sevice.find(municipio => municipio.nombre === nombre);
    if (municipio === undefined) {
      // Retorna un valor predeterminado, o lanza una excepción según tu caso de uso
      throw new Error(`Municipio con nombre ${nombre} no encontrado`);
    }
    return municipio;
  }

  public set_distancia_actual(nueva_distancia:number){
    this.distanciaActual = nueva_distancia;
  }
}
