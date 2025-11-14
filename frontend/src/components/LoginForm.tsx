import type { ComponentProps } from 'react';
import { Link, useNavigate } from 'react-router';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

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
    FieldDescription,
    FieldError,
    FieldGroup,
    FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { useLogin } from '@/auth/useLogin';
import { loginSchema, type LoginFormValues } from '@/auth/schema/login-schema.ts';
import { Spinner } from '@/components/ui/spinner';

export function LoginForm({ className, ...props }: ComponentProps<'div'>) {
    const login = useLogin();
    const navigate = useNavigate();

    const form = useForm<LoginFormValues>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: '',
            password: '',
        },
    });

    function onSubmit(values: LoginFormValues) {
        login.reset();
        login.mutate(values, {
            onSuccess: () => {
                navigate('/dashboard');
            },
        });
    }

    const formError = login.error instanceof Error ? login.error.message : null;

    return (
        <div className={cn('flex flex-col gap-6', className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Connectez-vous à votre compte</CardTitle>
                    <CardDescription>
                        Entrez votre adresse email ci-dessous pour vous connecter à votre compte
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-6"
                        noValidate
                    >
                        <FieldGroup>
                            <Controller
                                name="email"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="email">Adresse email</FieldLabel>
                                        <Input
                                            {...field}
                                            id="email"
                                            type="email"
                                            placeholder="simon.pierre@example.com"
                                            aria-invalid={fieldState.invalid}
                                            disabled={login.isPending}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
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
                                            <Link
                                                to="/forgot-password"
                                                className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                                            >
                                                Mot de passe oublié ?
                                            </Link>
                                        </div>
                                        <Input
                                            {...field}
                                            id="password"
                                            type="password"
                                            aria-invalid={fieldState.invalid}
                                            disabled={login.isPending}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            {formError && (
                                <Field data-invalid>
                                    <FieldError errors={[{ message: formError }]} />
                                </Field>
                            )}

                            <Field>
                                <Button type="submit" disabled={login.isPending} className="w-full">
                                    {login.isPending && <Spinner />}
                                    {login.isPending ? 'Connexion...' : 'Se connecter'}
                                </Button>
                                <FieldDescription className="text-center">
                                    Vous n&apos;avez pas de compte ? <Link to="/register">S&apos;inscrire</Link>
                                </FieldDescription>
                            </Field>
                        </FieldGroup>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
