import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapScreenComponent } from './Mapas/screens/map-screen/map-screen.component';
import { FormsComponent } from './Mapas/screens/forms/forms.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MapScreenComponent,FormsComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'mapa';
}
