import { NgModule } from "@angular/core";
import { MatInputModule } from "@angular/material/input"
import { MatButtonModule } from "@angular/material/button"
import { MatIconModule } from "@angular/material/icon"


@NgModule({
    imports: [
        MatInputModule, 
        MatButtonModule,
        MatIconModule,
    ],
    exports: [
        MatInputModule, 
        MatButtonModule,
        MatIconModule,
    ]
})
export class MaterialModule { }