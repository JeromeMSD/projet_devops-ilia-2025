import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    Field,
    FieldDescription, FieldError,
    FieldGroup,
    FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import React from 'react';
import { useLogin } from '@/auth/useLogin.ts';
import { useNavigate } from 'react-router';
import { Controller, useForm } from 'react-hook-form';
import { type LoginFormValues, loginSchema } from '@/auth/login-schema.ts';
import { zodResolver } from '@hookform/resolvers/zod';

export function LoginForm({
                              className,
                              ...props
                          }: React.ComponentProps<'div'>) {
    const login = useLogin();
    const navigate = useNavigate();

    const form = useForm<LoginFormValues>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            username: '',
            password: '',
        },
    });

    async function onSubmit(values: LoginFormValues) {
        login.mutate(values, {
            onSuccess: () => {
                navigate('/dashboard');
            },
        });
    }

    return (
        <div className={cn('flex flex-col gap-6', className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Connectez-vous à votre compte</CardTitle>
                    <CardDescription>
                        Entrez votre nom d'utilisateur ci-dessous pour vous connecter à votre compte
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={form.handleSubmit(onSubmit)}>
                        <FieldGroup>
                            <Controller
                                name="username"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="username">Nom d'utilisateur</FieldLabel>
                                        <Input
                                            {...field}
                                            id="username"
                                            type="text"
                                            placeholder="johndoe"
                                            aria-invalid={fieldState.invalid}
                                            required
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]}/>
                                        )}
                                    </Field>
                                )}
                            />
                            <Controller
                                name="password"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <div className="flex items-center">
                                            <FieldLabel htmlFor="password">Mot de passe</FieldLabel>
                                            <a
                                                href="#"
                                                className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                                            >
                                                Mot de passe oublié ?
                                            </a>
                                        </div>
                                        <Input
                                            {...field}
                                            id="password"
                                            type="password"
                                            aria-invalid={fieldState.invalid}
                                            required
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]}/>
                                        )}
                                    </Field>
                                )}
                            />
                            <Field>
                                <Button type="submit">Se connecter</Button>
                                <FieldDescription className="text-center">
                                    Vous n&apos;avez pas de compte ? <a href="#">S&apos;inscrire</a>
                                </FieldDescription>
                            </Field>
                        </FieldGroup>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}