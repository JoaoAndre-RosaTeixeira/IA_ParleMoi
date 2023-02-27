import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {AccueilComponent} from "./accueil/accueil.component";
import {ChatBotComponent} from "./chat-bot/chat-bot.component";

const routes: Routes = [
  { path: 'accueil', component: AccueilComponent },
  { path: 'chat-bot', component: ChatBotComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
