import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { MapaService } from '../../services/mapa.service';
import { Municipio } from '../../interfaces/Municipio.interface';

@Component({
  selector: 'app-forms',
  standalone: true,
  imports: [],
  templateUrl: './forms.component.html',
  styleUrl: './forms.component.css'
})
export class FormsComponent implements AfterViewInit {
  constructor(private mapaService: MapaService){}

  @ViewChild("origen") origenInput!:ElementRef<HTMLInputElement>
  @ViewChild("destino") destinoInput!:ElementRef<HTMLInputElement>
  @ViewChild("algoritmo") algoritmoSelect!:ElementRef<HTMLSelectElement>

  recorridoTextArea: String = "";
  distanciaTextArea: number = 0;

  ngAfterViewInit(): void {
    if (!this.algoritmoSelect || !this.origenInput || !this.destinoInput) {
      console.error('Algunos elementos ViewChild no están disponibles');
    }
  }

  get origenYDestino():String[]{
    return this.mapaService.origenYDestino;
  }

  public calcular_ruta(){
    const origen: string = this.origenInput.nativeElement.value;
    const destino: string = this.destinoInput.nativeElement.value;
    const algoritmo: string = this.algoritmoSelect.nativeElement.value;

    const municipioOrigen: Municipio = this.mapaService.buscar_municipio(origen);
    const municipioDestino:Municipio = this.mapaService.buscar_municipio(destino);
    
    this.mapaService.get_recorrido([municipioOrigen,municipioDestino],algoritmo)?.subscribe({
      next:(resData)=>{
        this.recorridoTextArea = resData["recorrido"].join(" -> ").replaceAll("_", " ");
        this.distanciaTextArea = resData["distancia"];
        this.mapaService.setRecorrido(resData["recorrido"]);
        this.mapaService.set_distancia_actual(resData["distancia"])
      }
    })
  }
}
