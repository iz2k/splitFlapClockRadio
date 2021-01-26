import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {WeatherComponent} from './weather/weather.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {HistoricComponent} from './historic/historic.component';
import {SensorsComponent} from './sensors/sensors.component';
import {ClockComponent} from './clock/clock.component';
import {RadioComponent} from './radio/radio.component';
import {SpotifyComponent} from './spotify/spotify.component';


const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'clock', component: ClockComponent },
  { path: 'radio', component: RadioComponent },
  { path: 'spotify', component: SpotifyComponent },
  { path: 'sensors', component: SensorsComponent },
  { path: 'weather', component: WeatherComponent },
  { path: 'historic', component: HistoricComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
