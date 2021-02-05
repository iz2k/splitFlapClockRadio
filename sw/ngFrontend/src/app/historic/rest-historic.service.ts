import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestHistoricService {


  constructor(private backend: BackendService){}

  getMeasurements(filter): Observable<any> {
    return this.backend.post('/rest/historic/get-measurements', filter);
  }


}
