@Controller('users')
export class UserController extends BaseController implements OnInit {
  constructor(private readonly userService: UserService) {}

  @Get()
  getAll(): Promise<User[]> {
    return this.userService.findAll();
  }

  @Post()
  create(@Body() userDto: CreateUserDto): Promise<User> {
    return this.userService.create(userDto);
  }
}
