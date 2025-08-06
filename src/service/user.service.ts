import { Injectable } from '@nestjs/common';
import { CreateUserDto } from '../dto/create-user.dto';

@Injectable()
export class UserService {
  create(dto: CreateUserDto): string {
    return 'User created';
  }

  getAll(): string[] {
    return ['User1', 'User2'];
  }
}
