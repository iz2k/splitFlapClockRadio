import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { WeatherComponent } from './weather/weather.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import {SocketIoModule} from 'ngx-socket-io';
import {BackendService} from './backend.service';
import {HttpClientModule} from '@angular/common/http';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule } from '@angular/material/input';
import {JSBAngularFlipClockModule} from 'jsb-angular-flip-clock';
import {MatNativeDateModule} from '@angular/material/core';
import {MomentTimezonePickerModule} from 'moment-timezone-picker';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatSelectModule} from '@angular/material/select';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import { WeatherCurrentComponent } from './weather/weather-current/weather-current.component';
import { SensorsCurrentComponent } from './sensors/sensors-current/sensors-current.component';
import { HistoricComponent } from './historic/historic.component';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {ChartsModule} from 'ng2-charts';
import 'hammerjs';
import 'chartjs-plugin-zoom';
import { SensorsComponent } from './sensors/sensors.component';
import { SensorCalibrationComponent } from './sensors/sensor-calibration/sensor-calibration.component';
import { LocationComponent } from './location/location.component';
import { ClockComponent } from './clock/clock.component';
import { RadioComponent } from './radio/radio.component';
import { SpotifyComponent } from './spotify/spotify.component';
import { LocationConfigComponent } from './location/location-config/location-config.component';
import { ClockCurrentComponent } from './clock/clock-current/clock-current.component';
import { ClockCalibrateComponent } from './clock/clock-calibrate/clock-calibrate.component';
import { ClockAlarmsComponent } from './clock/clock-alarms/clock-alarms.component';
import {CalSplitFlapComponent} from './clock/clock-calibrate/cal-split-flap/cal-split-flap.component';
import { RadioCurrentComponent } from './radio/radio-current/radio-current.component';
import { RadioListComponent } from './radio/radio-list/radio-list.component';
import {NgxGaugeModule} from 'ngx-gauge';
import { SpotifyCurrentComponent } from './spotify/spotify-current/spotify-current.component';
import { SpotifyListComponent } from './spotify/spotify-list/spotify-list.component';
import { AlarmBriefComponent } from './clock/clock-alarms/alarm-brief/alarm-brief.component';
import { AlarmConfigComponent } from './clock/clock-alarms/alarm-config/alarm-config.component';
import {MatDialogModule} from "@angular/material/dialog";


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    WeatherComponent,
    DashboardComponent,
    WeatherCurrentComponent,
    SensorsCurrentComponent,
    HistoricComponent,
    SensorsComponent,
    SensorCalibrationComponent,
    LocationComponent,
    ClockComponent,
    RadioComponent,
    SpotifyComponent,
    LocationConfigComponent,
    ClockCurrentComponent,
    ClockCalibrateComponent,
    ClockAlarmsComponent,
    CalSplitFlapComponent,
    RadioCurrentComponent,
    RadioListComponent,
    SpotifyCurrentComponent,
    SpotifyListComponent,
    AlarmBriefComponent,
    AlarmConfigComponent
  ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        AppRoutingModule,
        JSBAngularFlipClockModule,
        NgbModule,
        SocketIoModule,
        HttpClientModule,
        MatFormFieldModule,
        MatInputModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatSelectModule,
        MatButtonModule,
        MatCheckboxModule,
        MatSlideToggleModule,
        MatIconModule,
        MatButtonToggleModule,
        ReactiveFormsModule,
        MomentTimezonePickerModule,
        FormsModule,
        ChartsModule,
        NgxGaugeModule,
        MatDialogModule
    ],
  providers: [BackendService],
  bootstrap: [AppComponent]
})
export class AppModule { }
