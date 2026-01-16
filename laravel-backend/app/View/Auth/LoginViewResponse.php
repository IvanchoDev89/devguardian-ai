<?php

namespace App\View\Auth;

use Laravel\Fortify\Contracts\LoginViewResponse as LoginViewResponseContract;
use Illuminate\Http\Response;

class LoginViewResponse extends Response implements LoginViewResponseContract
{
    public function toResponse($request)
    {
        return response()->view('auth.login');
    }
}
