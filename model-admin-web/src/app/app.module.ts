import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ModelManagementComponent } from './model-management/model-management.component';
import { FileUploadModule } from "primeng/fileupload";
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { FormsModule } from '@angular/forms';
import { TagModule } from 'primeng/tag';
import { DataViewModule } from 'primeng/dataview';
import { DialogModule } from 'primeng/dialog';
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { ProgressBarModule } from 'primeng/progressbar';
import { ToastModule } from 'primeng/toast';

@NgModule({
  declarations: [
    AppComponent,
    ModelManagementComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FileUploadModule,
    InputTextModule,
    ButtonModule,
    FormsModule,
    TagModule,
    DataViewModule,
    DialogModule,
    NoopAnimationsModule,
    ProgressBarModule,
    ToastModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
