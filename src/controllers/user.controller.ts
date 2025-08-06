// src/controllers/user.controller.ts
import { Controller, Get, Post } from '@nestjs/common';

@Controller('user')
export class UserController {
  @Get()
  getAllUsers(): string {
    return 'All users';
  }

  @Post()
  createUser(): string {
    return 'User created';
  }
}
